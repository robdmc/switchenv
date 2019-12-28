#! /usr/bin/env python

import os
import sys
import time
import click
from typing import Optional


def run_switch_env(profile: Optional[str] = None):
    print('Switchimng to profile', profile)


@click.group()
def cli():
    pass


@cli.command(help='List all profile names')
def list():
    click.echo('ls')


@cli.command(help='Show contents of a single profile')
def show():
    click.echo('show')


@cli.command(help='Delete a profile')
def delete():
    click.echo('delete')


# @cli.command()
# @click.argument('name')
# def activate(name):
#     run_switch_env(name)


@cli.command(help='Create a profile from file')
@click.option('-p', '--profile_name')
@click.option('-f', '--file_name')
def create(profile, file_name):
    pass

# @click.command()
# @click.argument('profile')
# @click.argument('ls')
# @click.option('-f', '--file')
# def main(profile: str, ls: bool, file: Optional[str] = None):
#     pass


if __name__ == '__main__':
    if len(sys.argv) > 1:
        cli()
    else:
        run_switch_env()
