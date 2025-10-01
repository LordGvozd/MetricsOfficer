from pathlib import Path

from officer import config
from officer.linter import Linter
from officer.metrics.checkers import get_all_metrics_checkers
from argparse import ArgumentParser


def run() -> None:
    parser = ArgumentParser(
        prog="Metrics Officer",
    )

    parser.add_argument("lint_path")

    settings_parser = config.SettingsParser(current_dir="./")
    settings_parser.add_argparser(parser)

    cli_args = parser.parse_args()

    settings = settings_parser.get_settings(cli_args)
    checkers = get_all_metrics_checkers(settings)

    linter = Linter(Path(cli_args.lint_path), checkers)
    linter.run()
