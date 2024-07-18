import asyncio
import logging
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path

from bot.main import run_application


@dataclass(frozen=True, slots=True)
class CliArgs:
    run: bool
    config: Path


def create_argparse() -> ArgumentParser:
    argparse = ArgumentParser(description='bot cli')
    run_group = argparse.add_argument_group(title='run')
    run_group.add_argument(
        '--run',
        action='store_true',
    )
    run_group.add_argument(
        '--config',
        dest='config',
        type=Path,
    )
    return argparse


def main() -> None:
    argparse = create_argparse()
    raw_data = argparse.parse_args().__dict__
    args = CliArgs(
        run=raw_data['run'],
        config=raw_data['config'],
    )
    
    logging.basicConfig(level=logging.DEBUG)
    if args.run:
        asyncio.run(run_application(args.config))
