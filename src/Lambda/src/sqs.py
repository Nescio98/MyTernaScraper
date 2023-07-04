import boto3
from message import Message

# Session is not needed if you run this on FARGATE with the right IAM role
session = boto3.Session(profile_name='default')

client = session.client('sqs', region_name='eu-west-1')

queue_url = 'https://sqs.eu-west-1.amazonaws.com/0923368/test-scraper-tso'


msg_list = [Message(2020, i, 'a', True) for i in range(1,13)]


for msg in msg_list:
    response = client.send_message(
        QueueUrl=queue_url,
        MessageBody=msg.to_json()
        )
pass


while True:
    response = client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=5,
        WaitTimeSeconds=10
    )

    if 'Messages' not in response:
        break

    for m in response['Messages']:
        msg = Message.from_json(m['Body'])
        reciept_handle = m['ReceiptHandle']

        print(msg)

        # Do whatever you want with the message

        response = client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=reciept_handle
            ) 

pass
