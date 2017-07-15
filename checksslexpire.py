#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import socket
import datetime
import time
import boto3
import ssl

def check_expiry():
    # Check the DNS name
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=HOST,
    )
    # 3 second timeout because Lambda has runtime limitations
    conn.settimeout(3.0)

    conn.connect((HOST, 443))
    ssl_info = conn.getpeercert()

    expiration_date = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
    expiration = (expiration_date - datetime.datetime.now()).days

    host_to_be_expired = {}

    if expiration <= DAYS:
        host_to_be_expired[HOST] = expiration
    else:
    # this else is just while testing
        host_to_be_expired[HOST] = expiration

def send_email_notification(host_to_be_expired):
    sns = boto3.resource("sns")
    topic = sns.Topic("arn:aws:sns:us-east-1:527728718473:ssl-expiry-check-lambda")
    topic.publish(
    Message=create_email_message(host_to_be_expired),
    MessageStructure="string"
    )

def create_email_message(host_to_be_expired):
    message = "The following customers' SSL certification will expire in less than " + str(DAYS) + " days:\n"
    for host, expire_days in host_to_be_expired.items():
        message = message + host + " expires in: " + str(expire_days) + " days"  +"\n"
    return message

def main(event, context):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--days', help='specify expiry days to send email', type=int, default=30)
    parser.add_argument('-p', '--port', help='specify a port to connect to', type=int, default=443)
    args = parser.parse_args()

    global HOST, DAYS, PORT
    PORT = args.port
    DAYS = args.days
    HOST = ''

    with open ("domainlist") as host_list:
        for line in host_list:
            line = line[:-1] # removes empty line added at the end
            HOST = line
            print(line)
            check_expiry()
    if len(HOST_TO_BE_EXPIRED) > 0:
        send_email_notification(HOST_TO_BE_EXPIRED)

if __name__ == "__main__":
    main()
