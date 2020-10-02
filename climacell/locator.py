from typing import Union
from opencage.geocoder import OpenCageGeocode as Locate

from climacell.config import cnf
from climacell.exceptions import OpenCageApiTypeError


class Locator:
    """
    Find coordinates of a place based
    on a query string

    :param location: The location which the coordinates are needed.
    """
    def __init__(self, location: str) -> None:
        if not cnf.opencage_key:
            raise Exception
        self.client = Locate(cnf.opencage_key)
        self.location = location

    def locate(self) -> Union[dict, list]:
        return self.client.geocode(self.location)

    @property
    def coordinates(self) -> tuple:
        location = self.locate()
        if not isinstance(location, list):
            raise OpenCageApiTypeError
        return tuple(self.locate()[0]['geometry'].values())
