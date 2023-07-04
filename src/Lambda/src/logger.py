import os
import sys
from logging import StreamHandler

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
    """
    Initialize the loggers and handlers.

    Parameters:
        loggerLevel (int): Level for the main logger
        consoleLoggerLevel (int): Level for the console logger
        customLoggerLevel (int): Level for the custom logger
        logPath (str, optional): Path to the log file. Defaults to None.
        fileName (str, optional): Name of the log file. Defaults to "amr".

    Returns:
        tuple: Tuple containing the formatter, logger, and consoleHandler objects
    """
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

    return formatter, logger, consoleHandler


_, logger, _ = initializeLogs(LOGGER_LEVEL, CONSOLE_LOGGER_LEVEL, EGO_LOGGER_LEVEL)
