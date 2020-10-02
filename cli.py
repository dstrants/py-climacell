import click
import os
from typing import Iterable, Optional

cli_folder = os.path.join(os.path.dirname(__file__), "cli")


class ClimaCellCli(click.MultiCommand):
    """Parent class of the cli"""

    def list_commands(self, ctx: click.Context) -> Iterable[str]:
        rv = []
        for filename in os.listdir(cli_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx: click.Context, cmd_name: str) -> Optional[click.Command]:
        ns = {}
        fn = os.path.join(cli_folder, cmd_name + '.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']


cli = ClimaCellCli(help="Checking the weather in style.")
if __name__ == "__main__":
    cli()
