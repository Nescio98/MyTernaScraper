from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class Environment:
    """
    Environment configuration class.
    """

    environment: str
    aws_default_region: str
    destination_bucket: str
    local_path: str
    queue_name: str

    @staticmethod
    def factory(environment: str, aws_default_region: str, destination_bucket: str, local_path: str, queue_name: str = ''):
        """
        Factory method to create a new Environment instance.

        Parameters
        ----------
        environment : str
            The environment name.
        aws_default_region : str
            The default AWS region.
        destination_bucket : str
            The bucket name for storing the downloaded data.
        local_path : str
            The local path where the downloaded data will be stored.
        queue_name : str, optional
            The name of the queue, by default ''.

        Returns
        -------
        Environment
            A new instance of the Environment class.

        """
        return Environment(environment, aws_default_region, destination_bucket, local_path, queue_name)
