import json
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from typing import List
import boto3
from message import Message
from database import get_plants
from logger import logger


def make_monthly_queue_list(plant_list: List[tuple], year: str, month: str, historical: bool):
    """
    Create a list of messages for each plant in the given month.

    Parameters:
        plant_list (List[tuple]): List of plant tuples containing (plant_id, plant_name)
        year (str): Year
        month (str): Month
        historical (bool): Flag indicating historical data

    Returns:
        List[Message]: List of messages for each plant in the specified month
    """
    return [Message(year, month, plant[0], plant[1], historical) for plant in plant_list]


def get_queue_url(aws_account_id: str, aws_region: str, queue_name: str):
    """
    Get the URL of the specified queue.

    Parameters:
        aws_account_id (str): AWS account ID
        aws_region (str): AWS region
        queue_name (str): Queue name

    Returns:
        str: URL of the queue
    """
    client = boto3.client('sqs', region_name=aws_region)
    response = client.get_queue_url(
        QueueName=queue_name,
        QueueOwnerAWSAccountId=aws_account_id
    )
    return response['QueueUrl']


def send_to_queue(queue_url: str, msg_list: List[Message]):
    """
    Send messages to the specified queue.

    Parameters:
        queue_url (str): URL of the queue
        msg_list (List[Message]): List of messages to send
    """
    client = boto3.client('sqs', region_name='eu-west-1')
    for msg in msg_list:
        response = client.send_message(
            QueueUrl=queue_url,
            MessageBody=msg.to_json()
        )
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.error(f"Error sending message to queue: {response}")
        else:
            logger.info(f"Message sent to queue: {msg.to_json()}")


def run_fargate_tasks(company: str, historical: bool, aws_region: str, environment: str, queue_name: str, destination_bucket: str, count: int):
    """
    Run Fargate tasks for the specified parameters.

    Parameters:
        company (str): Company name
        historical (bool): Flag indicating historical data
        aws_region (str): AWS region
        environment (str): Environment
        queue_name (str): Queue name
        destination_bucket (str): Destination bucket
        count (int): Number of tasks to run

    Returns:
        dict: Response from the run_task API call
    """
    client = boto3.client('ecs', region_name=aws_region)
    response = client.run_task(
        cluster='default',
        launchType='FARGATE',
        taskDefinition='staging-my-terna-metering',
        count=count,
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    'subnet-06ebac2073d4',
                ],
                'securityGroups': [
                    'sg-0c93de72c151',
                ],
                'assignPublicIp': 'ENABLED'
            }
        },
        overrides={
            'containerOverrides': [
                {
                    'name': 'staging-my-terna-metering',
                    'environment': [
                        {
                            'name': 'COMPANY',
                            'value': company
                        },
                        {
                            'name': 'ENVIRONMENT',
                            'value': environment
                        },
                        {
                            'name': 'DESTINATION_BUCKET',
                            'value': destination_bucket
                        },
                        {
                            'name': 'AWS_DEFAULT_REGION',
                            'value': aws_region
                        },
                        {
                            'name': 'QUEUE_NAME',
                            'value': queue_name
                        }

                    ]
                },
            ]
        }
    )
    return response


def run(company: str, historical: bool, aws_region: str, queue_url: str, bucket_name: str, fill_queue: bool, count: int = 1):
    """
    Run the data processing workflow.

    Parameters:
        company (str): Company name
        historical (bool): Flag indicating historical data
        aws_region (str): AWS region
        queue_url (str): URL of the queue
        bucket_name (str): Destination bucket name
        fill_queue (bool): Flag indicating whether to fill the queue
        count (int, optional): Number of tasks to run. Defaults to 1.
    """
    companies = get_plants(company)
    if fill_queue:
        if historical:
            today = datetime.today().date()
            time_reference = today - relativedelta(months=60)
            while time_reference < today:
                msg_list = make_monthly_queue_list(companies, str(
                    time_reference.year), str(time_reference.month).zfill(2), historical)
                send_to_queue(queue_url, msg_list)
                time_reference = time_reference + relativedelta(months=1)
        else:
            time_reference = datetime.today().date() - relativedelta(months=1)
            msg_list = make_monthly_queue_list(companies, str(
                time_reference.year), str(time_reference.month).zfill(2), historical)
            send_to_queue(queue_url, msg_list)

    run_fargate_tasks(company, historical, aws_region, os.environ["ENVIRONMENT"], os.environ["QUEUE_NAME"], bucket_name, count)


def input_parser(event):
    """
    Parse the input event and extract relevant parameters.

    Parameters:
        event (dict): Input event

    Returns:
        tuple: Tuple containing parsed parameters (historical, company, destination_bucket, fill_queue, region, environment, queue_url)
    """
    historical = event["Historical"]
    company = event["Company"]
    queue_name = event["QueueName"]
    destination_bucket = event["DestinationBucket"]
    fill_queue = event["FillQueue"]

    region = os.environ['AWS_DEFAULT_REGION']
    aws_account_id = os.environ['AWS_ACCOUNT_ID']
    environment = os.environ["ENVIRONMENT"]

    queue_url = get_queue_url(aws_account_id, region, queue_name)

    return historical, company, destination_bucket, fill_queue, region,  environment, queue_url


def handler(event, context):
    """
    Lambda handler function.

    Parameters:
        event (dict): Input event
        context (object): Lambda context object

    Returns:
        dict: Response containing the status code and a message
    """
    historical, company, destination_bucket, fill_queue, region,  environment, queue_url = input_parser(
        event)
    run(company, historical, region, queue_url,
        destination_bucket, fill_queue, 8)

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }


if __name__ == '__main__':
    handler({"Historical": True,
            "Company": "EGO Energy",
            "QueueName": "test-scraper-tso",
            "DestinationBucket": "ego-metering-tso-0921324368-eu-west-1",
            "FillQueue": True},
            None)
