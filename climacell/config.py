from pydantic import BaseSettings, Field


"""
Configuration Module.

It is based on pydantic and is responsible for parsing `.env` file
and loading parameters to make classes initiation easier.
"""

# TODO: Conditionally add more fields when available.
FIELDS = ["temp", "feels_like", "humidity", "wind_speed", "wind_direction",
          "baro_pressure", "precipitation", "sunrise", "sunset", "visibility", "weather_code"]


class ClimaCellSettings(BaseSettings):
    """
    Configuration wrapper to initiate the app.
    """
    base_url: str = "https://api.climacell.co/v3/"
    clima_fields: list = FIELDS
    clima_key: str = Field(..., env="CLIMACELL_KEY")
    opencage_key: str = Field("", env="OPENCAGE_KEY")
    unit_system: str = Field("si", env='CLIMACELL_UNIT_SYSTEM')

    class Config:
        env_file = ".env"


cnf = ClimaCellSettings()
