import logging
import os
import json
import boto3
import sys
import subprocess
from logging import StreamHandler
from botocore.exceptions import ClientError
from typing import Dict, List
from application.library.new_metadata_parser import parse, rup, version
from application.library.message import Message

# This variables are defined in serverless:
# ENVIRONMENT
# SERVICE_NAME
# TODO: da mettere a posto (non ci dovrebbero essee riferimeti espliciti al env)
REGION = os.environ["AWS_DEFAULT_REGION"]

CONSOLE_LOGGER_LEVEL = logging.DEBUG
LOGGER_LEVEL = logging.DEBUG
EGO_LOGGER_LEVEL = 100  # logging.ERROR


class EGOHandler(StreamHandler):
    def __init__(self):
        StreamHandler.__init__(self)

    # def emit(self, record):
    #     msg = self.format(record)
    #     msg=msg.replace("'","\"")
    #     subj="Job " + SERVICE_NAME + ":{0} returned ERROR.".format(ENVIRONMENT)
    #     transmitAlert(msg, "email", EMAIL_RECIPIENTS, SERVICE_NAME, subj)


def initializeLogs(
    loggerLevel, consoleLoggerLevel, customLoggerLevel, logPath=None, fileName="amr"
):
    # initializing logging formatter
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")

    # initializing logger
    logger = logging.getLogger(__name__)
    logger.setLevel(loggerLevel)

    # initializing console handler for logging
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setLevel(consoleLoggerLevel)
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

    # adding custom handler
    egohandler = EGOHandler()
    egohandler.setLevel(customLoggerLevel)
    egohandler.setFormatter(formatter)
    logger.addHandler(egohandler)

    logger.propagate = False

    return (
        formatter,
        logger,
        consoleHandler,
    )


_, logger, _  = initializeLogs(LOGGER_LEVEL, CONSOLE_LOGGER_LEVEL, EGO_LOGGER_LEVEL)


def upload_file(file_name, bucket, s3client, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param s3client: Boto3 S3 client
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        response = s3client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_parameters(parameters):
    """Get variables from AWS parameter store

    :param parameters: List of parameters to retrieve
    """
    ssm_client = boto3.client("ssm", region_name=REGION)
    return ssm_client.get_parameters(Names=parameters, WithDecryption=True)




def list_keys_from_s3(bucket_name: str, prefix: str):
    """
    List the object key in an S3 bucket filtered for a specific prefix. 
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    for object in bucket.objects.filter(Prefix=prefix, Delimiter='/'):
        if object.key.endswith('/'):
            continue
        yield object.key


def already_on_s3(bucket_name: str, prefix: str) -> Dict[str, int]:
    """
    Retrieve a dictionary of keys and versions for objects already present in an S3 bucket.

    Parameters
    ----------
    bucket_name : str
        Name of the S3 bucket.
    prefix : str
        Prefix for the objects in the bucket.

    Returns
    -------
    Dict[str, int]
        A dictionary where keys are parsed object names and values are their respective versions.

    """
    keys = list_keys_from_s3(bucket_name, prefix)
    return {rup(p): version(p) for p in map(parse, keys)}


def get_missing(uploaded_on_S3: Dict[str, int], plants: List[Dict]) -> List[Dict]:
    """
    Get a list of plants that are missing from the S3 bucket based on their versions.

    Parameters
    ----------
    uploaded_on_S3 : Dict[str, int]
        A dictionary containing the names of plants uploaded on S3 as keys and their respective versions as values.
    plants : List[Dict]
        A list of dictionaries representing plants, where each dictionary contains information about a plant,
        including 'codiceUp' (plant name) and 'versione' (plant version).

    Returns
    -------
    List[Dict]
        A list of dictionaries representing the plants that are missing from the S3 bucket based on their versions.

    """
    if not uploaded_on_S3:
        return plants
    else:
        missing = [plant for plant in plants if not uploaded_on_S3.get(plant['codiceUp'], '') == plant['versione']]
        return missing
    
def make_monthly_queue_list(plant_list: List[Tuple], year: str, month: str) -> List[Message]:
    """
    Create a list of Message objects representing the monthly queue for plants.

    Parameters
    ----------
    plant_list : List[Tuple]
        A list of tuples representing plants, where each tuple contains information about a plant.
        The first element of the tuple is the plant's name and the second element is the plant's ID.
    year : str
        The year for which to create the monthly queue.
    month : str
        The month for which to create the monthly queue.

    Returns
    -------
    List[Message]
        A list of Message objects representing the monthly queue for plants.
        Each Message object contains information about the year, month, plant name, and plant ID.

    """
    return [Message(year, month, plant[0], plant[1]) for plant in plant_list]





