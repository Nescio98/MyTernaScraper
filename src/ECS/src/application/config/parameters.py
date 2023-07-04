from dataclasses import dataclass
from datetime import date
from dataclasses_json import dataclass_json

from typing import List


@dataclass_json
@dataclass(frozen=True)
class Parameters:
    """
    Application parameters class.
    """

    company: str

    @staticmethod
    def factory(company: str):
        """
        Factory method to create a new Parameters instance.

        Parameters
        ----------
        company : str
            The company name.

        Returns
        -------
        Parameters
            A new instance of the Parameters class.

        """
        return Parameters(company)
