from typing import List, Optional
import requests
import pendulum

from climacell.config import cnf
from climacell import exceptions as e
from climacell.locator import Locator as L


class ClimaCellApi:
    """
    Clima Cell Api Wrapper.

    The wrapper that's respnsible for performing all the API calls
    """
    def __init__(self, coords: Optional[tuple] = None, location: Optional[str] = None) -> None:
        self.api_key: str = cnf.clima_key
        self.base_url: str = cnf.base_url
        self.coords: tuple = self._set_coordinates(location, coords)
        self.fields: list = cnf.clima_fields
        self.unit_system: str = cnf.unit_system

    @staticmethod
    def _set_coordinates(location: Optional[str], coordinates: Optional[tuple]) -> tuple:
        """Sets the coordinates from the init params or raises exception."""
        if location:
            return L(location=location).coordinates
        elif coordinates:
            return coordinates
        raise e.ClimaCaseNoLocationError

    def call(self, endpoint: str = "", query: dict = dict(), method: str = "GET",
             unit: bool = True) -> dict:
        """Abstract method that performs the calls."""
        query.update({'apikey': self.api_key, 'lat': self.coords[0], 'lon': self.coords[1]})
        if unit:
            query['unit_system'] = self.unit_system
        resp = requests.request(
            url=self.base_url + endpoint,
            method=method,
            params=query
        )
        if not resp.ok:
            raise e.ClimaAPIError(resp)
        return resp.json()

    def realtime(self, fields: List[str] = list()) -> dict:
        """
        Real time observational data

        :param fields: List of strings. Selected fields from the data layers
        e.g. `humidity`
        """
        query = {
            "fields": fields or self.fields,
        }
        return self.call("weather/realtime", query)

    def nowcast(self, timestep: int = 5, start_time: str = "now",
                end_time: Optional[str] = None, fields: List[str] = list()) -> dict:
        """
            The nowcast call provides forecasting data on a minute-­by-­minute basis,
            based on ClimaCell’s proprietary sensing technology and models.

            :param timestep: The interval of the forecasting data in minutes (defaults to `5min`)
            :param start_time: The start time of the analysis.
            :param end_time: The end time of the analysis. Max >= 360 after the `start_time`
            :param fields: List of strings. Selected fields from the data layers e.g. `humidity`.
        """
        end_time = end_time or str(pendulum.parse(start_time).add(minutes=360))
        query = {
            "start_time": start_time,
            "end_time": end_time,
            "timestep": timestep,
            "fields": fields or self.fields
        }
        return self.call("weather/nowcast", query)

    def hourly(self, start_time: str = "now", end_time: Optional[str] = None,
               fields: List[str] = list()) -> dict:
        """
            The hourly call provides a global hourly forecast, up to 108 hours (4.5 days) out,
            for a specific location.

            :param start_time: The start time of the analysis.
            :param end_time: The end time of the analysis. Max >= 108 hours after the `start_time`
            :param fields: List of strings. Selected fields from the data layers e.g. `humidity`.
        """
        end_time = end_time or str(pendulum.parse(start_time).add(hours=108))
        query = {
            "start_time": start_time,
            "end_time": end_time,
            "fields": fields or self.fields
        }
        return self.call("weather/forecast/hourly", query)

    def daily(self, start_time: str = "now", end_time: Optional[str] = None,
              fields: List[str] = list()) -> dict:
        """
            The daily API call provides a global daily forecast with summaries up to 15 days out.

            :param start_time: The start time of the analysis.
            :param end_time: The end time of the analysis. Max >= 15 days after the `start_time`
            :param fields: List of strings. Selected fields from the data layers e.g. `humidity`.
        """
        end_time = end_time or str(pendulum.parse(start_time).add(days=15).start_of("day"))
        query = {
            "start_time": start_time,
            "end_time": end_time,
            "fields": fields or self.fields
        }
        return self.call("weather/forecast/daily", query)

    def climacell(self, start_time: Optional[str] = None, end_time: Optional[str] = "now",
                  timestep: int = 5, fields: List[str] = list()) -> dict:
        """
            ClimaCell’s proprietary historical weather information is provided
            up to 6 hours in the past.

            :param timestep: The interval of the historical data in minutes (defaults to `5min`)
            :param start_time: The start time of the analysis.
            :param end_time: The end time of the analysis. Max >= 360 after the `start_time`
            :param fields: List of strings. Selected fields from the data layers e.g. `humidity`.
        """
        start_time = start_time or str(pendulum.parse(end_time).subtract(minutes=360))
        query = {
            "start_time": start_time,
            "end_time": end_time,
            "timestep": timestep,
            "fields": fields or self.fields
        }
        return self.call("weather/historical/climacell", query)

    def station(self, start_time: Optional[str] = None, end_time: Optional[str] = "now",
                fields: List[str] = list()) -> dict:
        """
            Historical weather station information is provided globally from 4 weeks
            in the past to the present. United States METAR and additional stations are included.

            :param start_time: The start time of the analysis.
            :param end_time: The end time of the analysis. Max >= weeks hours after the `start_time`
            :param fields: List of strings. Selected fields from the data layers e.g. `humidity`.
        """
        start_time = start_time or str(pendulum.parse(end_time).subtract(minutes=360))
        fields = fields or self.fields
        for field in ('sunrise', 'sunset', 'weather_code'):
            if field in fields:
                fields.remove(field)
        query = {
            "start_time": start_time,
            "end_time": end_time,
            "fields": fields
        }
        return self.call("weather/historical/station", query)

    def fire_index(self):
        """
        The average wildfire risk for the exact location,
        given average climate conditions in the past 20 years.
        """
        return self.call("insights/fire-index", unit=False)
