import os
from typing import List
import boto3
import psycopg2

from logger import logger

aws_region = os.environ["AWS_DEFAULT_REGION"]


def get_parameters(parameters):
    """
    Get variables from AWS parameter store

    Parameters:
        parameters (List[str]): List of parameters to retrieve

    Returns:
        dict: A dictionary containing the retrieved parameters
    """
    ssm_client = boto3.client("ssm", region_name=aws_region)
    return ssm_client.get_parameters(Names=parameters, WithDecryption=True)


res = get_parameters(
    [
        "/prod/datalake/host",
        "/prod/datalake/database",
        "/prod/datalake/lambda/username",
        "/prod/datalake/lambda/password",
    ]
)


def get_aws_param():
    """
    Extracts relevant parameters from the retrieved parameters dictionary.

    Returns:
        tuple: A tuple containing host, database, username, and password
    """
    for p in res["Parameters"]:
        if "host" in p.get("Name"):
            host = p.get("Value")
        elif "database" in p.get("Name"):
            database = p.get("Value")
        elif "password" in p.get("Name"):
            password = p.get("Value")
        elif "username" in p.get("Name"):
            username = p.get("Value")

    return (host, database, username, password)


def get_db_connection(host: str, database: str, username: str, password: str):
    """
    Establishes a connection to the PostgreSQL database.

    Parameters:
        host (str): Host name or IP address of the database server
        database (str): Name of the database
        username (str): Username for authentication
        password (str): Password for authentication

    Returns:
        psycopg2.extensions.connection: A connection object to interact with the database
    """
    try:
        connection = psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=host,
            port=5432,
            connect_timeout=3,
        )
        return connection
    except (Exception, psycopg2.Error) as e:
        logger.exception(f"Cannot connect to database {database}", e)


def execute_query(connection, query):
    """
    Executes a SQL query on the given database connection.

    Parameters:
        connection (psycopg2.extensions.connection): Connection object to the database
        query (str): SQL query to execute

    Returns:
        list: A list containing the query results
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except (Exception, psycopg2.Error) as e:
        logger.exception("Error executing query", e)
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_plants(company: str):
    """
    Retrieves plants based on the provided company.

    Parameters:
        company (str): Company name

    Returns:
        list: A list of plants matching the given company
    """
    query = f""" SELECT
                "CodiceSAPR", "Rilevante" FROM
                zoho_crm."Impianti" WHERE
                "UnitàDisp.Come" = '{company}' AND
                "AttualmenteDisp.Terna?" = TRUE AND
                (("Rilevante" = TRUE) OR ("Rilevante" = FALSE AND "TensioneDiRete" = 'Alta')); """

    conn = get_db_connection(*get_aws_param())
    plants = execute_query(conn, query)
    return plants
