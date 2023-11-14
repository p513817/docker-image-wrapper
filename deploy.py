from typing import Tuple
import logging

import rich
from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler

from utils import (
    read_json,
    wait_seconds,
    wrap_service,
    build_args,
    get_image_name,
    DisableServiceError
)

# Constant

GREEN = "[green]"
RED = "[red]"
GRAY = "[bright_black]"
RESET = "[/]"

S_COMP = "PASS"
S_FAIL = "FAIL"
S_SKIP = "SKIP"

COMP = f"{GREEN}{S_COMP}{RESET}"
FAIL = f"{RED}{S_FAIL}{RESET}"
SKIP = f"{GRAY}{S_SKIP}{RESET}"

# Global
console = Console() 
console.clear()

# Rich

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%H:%M:%S]",
    handlers=[RichHandler(
        show_level=False,
        rich_tracebacks=True,
        console=console,
        show_path=False,
        markup=True)]
)
log = logging.getLogger("rich")

def set_color(word:str, color:str):
    return f"[{color}]{word}[/]"

def get_table( title: str, columns: list) -> rich.table.Table:
    """design rich table

    Args:
        title (str, optional): table's title.
        columns (list, optional): table's columns.

    Returns:
        rich.table.Table: rich table that supports console.print()
    """
    table = Table(  title=title,
                    show_header=True, 
                    header_style="bold magenta",
                    safe_box=True )
    [ table.add_column(col) for col in columns ]
    return table

def draw_config_table(config: dict):

    # Define table
    title = "Service Wrapper"
    columns = [ "Source", "Target ( Rename )", "Version", "Arch"]
    table = get_table(title, columns)

    # Update value
    for serv in config["services"]:
        table.add_row(
            serv["source"], 
            f"{config['username']}/{serv['target']}", 
            serv["version"],
            serv["arch"]
        )
    
    # Draw
    console.print(table)

def wrap_service_with_rich(config: dict):

    ( username, services ) = \
        [ config[k] for k in [ 'username', 'services' ] ]

    with console.status("[bold green] Wrapping service ...") as status:
        
        for serv in services:
            
            status, tc = S_SKIP, None
            
            source = get_image_name( serv["source"], serv["version"])
            target = get_image_name( serv["target"], serv["version"], username )
            arch = serv["arch"]

            if not bool(serv["enable"]):
                log.debug(f'{GRAY}{SKIP} ) {source} ... {RESET}')
                continue

            try:
                result, tc = wrap_service(source, target, arch)
                # result, tc = wait_seconds(1, not bool(serv["enable"]), not bool(serv["enable"]))
                log.info(f'{COMP} ) {source} -> {target} ( Cost: {tc}s )')

            except Exception as e:
                log.error(f'{FAIL} ) {e}')

def main(args):

    # Get config
    config = read_json(args.config)

    # Draw config table
    draw_config_table(config)

    # Start wrapping with rich table
    wrap_service_with_rich(config)

if __name__ == "__main__":
    main(build_args())