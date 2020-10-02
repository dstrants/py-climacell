import click
from rich import console
from rich import print
from rich.panel import Panel

from climacell.api import ClimaCellApi as Clima

cons = console.Console()

@click.group()
def cli() -> None:
    """Getting heather forecasts."""
    pass


@cli.command()
@click.argument("location", required=True, type=str)
def daily(location: str) -> None:
    """Returns the daily forecast."""
    clima = Clima(location=location)
    daily = clima.daily()
    print(Panel.fit(location, title="Daily Forecast"))
    for day in daily:
        temp = day['temp']
        cons.print(f"🌡 {temp[0]['min']['value']}C -> {temp[1]['max']['value']}C", style='bold magenta')


if __name__ == "__main__":
    cli()
