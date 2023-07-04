import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    """
    Represents a message composed by year, month, sapr,relevant and historical.
    """

    year: str
    month: str
    sapr: str
    relevant: bool
    historical: bool

    def to_json(self) -> str:
        """
        Convert the Message object to a JSON string.

        Returns
        -------
        str
            The JSON representation of the Message object.

        """
        return json.dumps(self.__dict__)
    
    @staticmethod
    def from_json(jobj: str) -> 'Message':
        """
        Create a Message object from a JSON string.

        Parameters
        ----------
        jobj : str
            The JSON string representing the Message object.

        Returns
        -------
        Message
            The created Message object.

        """
        return Message(**json.loads(jobj))
    

