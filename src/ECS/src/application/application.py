from application.config.config import Config
from application.config.environment import Environment
from application.config.parameters import Parameters

from application.library.main import run


class Application:
    """
    Represents an application that can be run in a specific environment with given parameters.
    """

    def __init__(self, environment: Environment, parameters: Parameters):
        """
        Initialize the Application object.

        Parameters
        ----------
        environment : Environment
            The environment in which the application will run.
        parameters : Parameters
            The parameters required for running the application.

        """
        self.environment = environment
        self.parameters = parameters

    def run(self) -> Any:
        """
        Run the application in the specified environment with the given parameters.

        Returns
        -------
        Any
            The result of running the application.

        """
        return run(self.environment, self.parameters)


def factory(config: Config) -> Application:
    """
    Create an Application object based on the provided configuration.

    Parameters
    ----------
    config : Config
        The configuration object containing environment and parameter details.

    Returns
    -------
    Application
        An instance of the Application class.

    """
    return Application(config.environment, config.parameters)
