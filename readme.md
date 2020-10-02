# ClimaCell Python Wrapper

A simple wrapper of [climacell api](https://developer.climacell.co/v3/reference#introduction).
For convinience this project also takes advantage of [opencage-python](https://github.com/OpenCageData/python-opencage-geocoder/) to find coordinates of the locations.

## Set Up

Run `pip install climacell` to install the package.

The for easy setup copy the `.env.example` to `.env` and add both (climacell and opencage) API keys. OpenCage is not neccecery but you have to insert coordinates yourself if you do not plan to use it.

Once you have your `.env` file ready you can move forward with using the package.

```py
from climacell.api import ClimaCellApi as Clima

# Initiate with location name (using opencage api)
c = Clima("Thessaloniki")

# Or pass the coordinates yourself
c = Clima(coords=(44.54, 22.24))

# Check the daily forcast
c.daily()
```
