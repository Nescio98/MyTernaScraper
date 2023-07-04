from dataclasses import dataclass

from .environment import Environment
from .parameters import Parameters


@dataclass
class Config:
    """
    Configuration class that holds environment and parameter information.
    """

    environment: Environment
    parameters: Parameters

    @staticmethod
    def factory(environment: Environment, parameters: Parameters):
        """
        Factory method to create a new Config instance.

        Parameters
        ----------
        environment : Environment
            An instance of the Environment class containing environment settings.
        parameters : Parameters
            An instance of the Parameters class containing input parameters.

        Returns
        -------
        Config
            A new instance of the Config class.

        """
        return Config(environment=environment, parameters=parameters)
