from typing_extensions import final
import psycopg2
from datetime import datetime

from application.library.shared import get_parameters, logger

# TODO: Da muovere in un helper
# TODO: gestire staging
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
    Get AWS parameters from the result dictionary.

    Returns
    -------
    tuple
        A tuple containing the host, database, username, and password.

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
    Establish a database connection.

    Parameters
    ----------
    host : str
        The database host.
    database : str
        The name of the database.
    username : str
        The username for the database connection.
    password : str
        The password for the database connection.

    Returns
    -------
    psycopg2.extensions.connection
        The database connection object.

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
    Execute a SQL query and retrieve the result.

    Parameters
    ----------
    connection : psycopg2.extensions.connection
        The database connection object.
    query : str
        The SQL query to execute.

    Returns
    -------
    list
        The result of the query.

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
    Retrieve plants based on the company.

    Parameters
    ----------
    company : str
        The company name.

    Returns
    -------
    list
        The list of plants.

    """
    query = f"""
        SELECT
            "CodiceSAPR", "Rilevante"
        FROM
            zoho_crm."Impianti"
        WHERE
            "UnitàDisp.Come" = '{company}' AND
            "AttualmenteDisp.Terna?" = TRUE; """
    conn = get_db_connection(*get_aws_param())
    plants = execute_query(conn, query)
    return plants


def get_downloaded_files(anno: int, mese: int, tipologia: str, dispacciato_da: str):
    """
    Get the downloaded files based on the specified parameters.

    Parameters
    ----------
    anno : int
        The year of the files.
    mese : int
        The month of the files.
    tipologia : str
        The type of the files.
    dispacciato_da : str
        The source of the files.

    Returns
    -------
    set
        A set of downloaded file names.

    """
    query = f"""
        SELECT
            "nome_file"
        FROM
            terna."downloaded_measure_files"
        WHERE
            "anno" = {anno} AND
            mese = {mese} AND
            "tipologia" = '{tipologia}' AND
            "dispacciato_da" = '{dispacciato_da}'; """
    conn = get_db_connection(*get_aws_param())
    measures = execute_query(conn, query)
    return set(list(zip(*measures))[0]) if len(measures) > 0 else set()


def write_measure(
    nome_file: str,
    anno: int,
    mese: int,
    tipologia: str,
    sapr: str,
    codice_up: str,
    codice_psv: str,
    vers: str,
    validazione: str,
    dispacciato_da: str,
):
    """
    Write measure information to the database.

    Parameters
    ----------
    nome_file : str
        The name of the file.
    anno : int
        The year of the measure.
    mese : int
        The month of the measure.
    tipologia : str
        The type of the measure.
    sapr : str
        The SAPR code.
    codice_up : str
        The UP code.
    codice_psv : str
        The PSV code.
    vers : str
        The version of the measure.
    validazione : str
        The validation status of the measure.
    dispacciato_da : str
        The source of the measure.

    """
    try:
        connection = get_db_connection(*get_aws_param())
        cursor = connection.cursor()
        query = f"""
          INSERT INTO terna."downloaded_measure_files" VALUES (
            '{nome_file}',
             {anno},
             {mese},
            '{tipologia}',
            '{sapr}',
            '{codice_up}',
            '{codice_psv}',
             {vers},
             {validazione},
            '{dispacciato_da}',
            '{datetime.utcnow()}'); """

        cursor.execute(query)
        connection.commit()
    except (Exception, psycopg2.Error) as e:
        logger.exception(
            f"Error when trying to insert downloaded measure file for {nome_file}", e
        )
    finally:
        if connection:
            cursor.close()
            connection.close()
