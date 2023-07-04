from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Message:
    """
    Represents a message.

    Args:
        year (str): Year of the message.
        month (str): Month of the message.
        sapr (str): SAPR value of the message.
        relevant (bool): Relevant status of the message.
        historical (bool): Historical status of the message.
    """

    year: str
    month: str
    sapr: str
    relevant: bool
    historical: bool

    def to_json(self) -> str:
        """
        Convert the message to JSON format.

        Returns:
            str: JSON representation of the message.
        """
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(jobj: str) -> 'Message':
        """
        Create a Message object from a JSON string.

        Args:
            jobj (str): JSON string representing the message.

        Returns:
            Message: Message object created from the JSON string.
        """
        return Message(**json.loads(jobj))




