

import click
import webbrowser

# from ..cli import console_log as log
# from .. import console_log as log

from ..read_pdf import read_pdf

#! =========================================
#! Setting up click
#! =========================================

#! - - - - - - - - - - - - - - - - - - - - -
#! Main click group


@click.group()
def main():
    pass

#! - - - - - - - - - - - - - - - - - - - - -
#! Run subgroup


@main.group(short_help="Executes a given command. Ask 'run --help' to learn more.", help="Executes one of the commands listed below.")
def run():
    pass

# read_pdf


@run.command(short_help="")
@click.option("--input-file", '-i', type=click.Path(exists=True, dir_okay=False), help="Input pdf file with data code to be read. ")
@click.option("--data-file", '-d', type=click.Path(exists=True, dir_okay=False), help="Input file with data")
def read(**kargs):
    return read_pdf(kargs)
