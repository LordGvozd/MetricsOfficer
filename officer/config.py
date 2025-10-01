from argparse import ArgumentParser, Namespace
import argparse
from pathlib import Path
from typing import Final, Mapping, Sequence, Set
from dataclasses import dataclass

from officer.models import MetricsError


@dataclass
class Settings:
    max_file_len: int = 200
    max_func_len: int = 50
    max_method_len: int = 30


class SettingsParser:
    def __init__(self, current_dir: str, config_path: str | None = None) -> None:
        self._settings = Settings()

    def add_argparser(self, argparser: ArgumentParser) -> None:
        for name, obj_type in Settings.__annotations__.items():
            arg_name = "--" + name.replace("_", "-")

            argparser.add_argument(
                arg_name, type=obj_type, default=getattr(Settings, name)
            )

    def _get_settings_from_cli(self, cli_args: Namespace) -> None:
        settings_annotations = Settings.__annotations__

        for name in settings_annotations:
            self._settings.__setattr__(name, getattr(cli_args, name))

    def get_settings(self, cli_args: Namespace) -> Settings:
        self._get_settings_from_cli(cli_args)

        return self._settings
