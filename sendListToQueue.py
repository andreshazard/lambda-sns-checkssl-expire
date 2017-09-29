import boto3


def lambda_handler(event, context):
    clients = ["training.contexti.com","academy.getbase.com","learning.efi.com",
    "academy.ethosgroup.com","university.gooddata.com","training.looker.com",
    "marketplace.servicerocket.com","training.prescience.com.au",
    "university.moogsoft.com","training.pentaho.com","university.sugarcrm.com",
    "training.couchbase.com","training.docker.com","learn.puppet.com",
    "university.nginx.com","training.saucelabs.com","training.mulesoft.com",
    "university.sailpoint.com","university.code42.com","kenshoou.com",
    "customersuccessuniversity.gainsight.com","training.chef.io"]

    sns = boto3.resource("sns")
    topic = sns.Topic("arn:aws:sns:us-west-2:527728718473:domainlist-queue")

    for client in clients:
        topic.publish(
	    Message=client
        )

    return 'Hello from Lambda'
