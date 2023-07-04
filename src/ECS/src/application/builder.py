from dataclasses import dataclass
import os
from distutils.util import strtobool

from application.config.config import Config
from application.config.environment import Environment
from application.config.parameters import Parameters

# TODO: Analizzare inpuut richiesti e modalità di esecuzione


class AppConfiguration:
    """
    Retrieves the application configuration from environment variables and/or command line arguments.
    """

    def get_environment(self) -> Environment:
        """
        Retrieve the environment configuration from environment variables.

        Returns
        -------
        Environment
            An instance of the Environment class containing the environment configuration.

        """
        environment = os.environ.get("ENVIRONMENT")
        aws_default_region = os.environ.get("AWS_DEFAULT_REGION")
        destination_bucket = os.environ.get("DESTINATION_BUCKET")
        local_path = os.environ.get("DOWNLOAD_PATH", "/app")
        queue_name = os.environ.get("QUEUE_NAME", "")

        return Environment.factory(
            environment=environment,
            aws_default_region=aws_default_region,
            destination_bucket=destination_bucket,
            local_path=local_path,
            queue_name=queue_name,
        )

    def get_parameters(self) -> Parameters:
        """
        Retrieve the parameters configuration from environment variables.

        Returns
        -------
        Parameters
            An instance of the Parameters class containing the parameters configuration.

        """
        company = os.environ.get("COMPANY", "")

        return Parameters.factory(
            company=company
        )

    def build(self) -> Config:
        """
        Build the configuration object.

        Returns
        -------
        Config
            A Config instance containing the configuration and parameters.

        """
        config = self.get_environment()
        parameters = self.get_parameters()
        return Config(config, parameters)
