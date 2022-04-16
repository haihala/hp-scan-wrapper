from __future__ import annotations

import argparse
from getpass import getpass
import json
from typing import Any

from translations import TRANSLATIONS


def load_config(path: str) -> dict[str, Any]:
    try:
        with open(path) as fp:
            return json.load(fp)
    except FileNotFoundError:
        return {}


class Config:
    # File where the config is written to and read from
    config_path: str

    # Where the images go
    target_dir: str

    # hp-scan scanner index
    device: str

    # Command to start the file explorer (presumes you can add a folder after this)
    file_explorer: str

    # Emails used previously are saved for quick access
    used_emails: list[str]

    # Format used to generate filenames with strftime
    date_format_string: str

    # Sender gmail address
    smtp_sender: str

    # Sender gmail password
    smtp_password: str

    # Which translations to use
    locale: str

    translations: dict[str, str]

    def __init__(self, args) -> None:
        ...
        # If config file from args exists, read it and supplement with args.
        # If it doesn't create it and populate with args

        # Where the config is loaded from
        default_config = self.default_config()
        self.config_path = args.config_path or default_config['config_path']

        config_file = load_config(self.config_path)

        for attribute in [
            'locale',   # Needs to be relatively high up
            'target_dir',
            'device',
            'file_explorer',
            'used_emails',
            'date_format_string',
            'smtp_sender',
            'smtp_password',
        ]:
            setattr(
                self,
                attribute,
                getattr(    # Command line
                    args,
                    attribute,
                    None,
                ) or   # Config file
                config_file.get(
                    attribute,
                ) or    # Global default
                default_config.get(
                    attribute,
                )
            )

            if getattr(self, attribute) is None:
                value = getpass(self.get_translation(f'setup_{attribute}'))
                setattr(self, attribute, value)

    def default_config(self) -> dict[str, Any]:
        return {
            'config_path': 'scanner_config.json',
            'target_dir': '~/Pictures',
            'device': '1',
            'used_emails': [],
            'date_format_string': '%A %d.%m.%Y %H:%M:%S.png',
            'locale': 'en',
            'file_explorer': 'thunar'
        }

    def write_config(self) -> None:
        with open(self.config_path, 'w') as file:
            json.dump(self.to_json(), file)

    def to_json(self) -> dict[str, Any]:
        return {
            'locale': self.locale,   # Needs to be relatively high up
            'target_dir': self.target_dir,
            'device': self.device,
            'file_explorer': self.file_explorer,
            'used_emails': self.used_emails,
            'date_format_string': self.date_format_string,
            'smtp_sender': self.smtp_sender,
            'smtp_password': self.smtp_password,
        }

    def print(self, key) -> None:
        print(self.get_translation(key))

    def get_translation(self, key) -> str:
        return TRANSLATIONS[self.locale][key]


def parse_args() -> Config:
    parser = argparse.ArgumentParser(description='Skannaustyökalu')
    parser.add_argument('--config_path')
    parser.add_argument('--target_dir')
    parser.add_argument('--device')
    parser.add_argument('--file_explorer')
    parser.add_argument('--date_format_string')
    parser.add_argument('--smtp_sender')
    parser.add_argument('--smtp_password')
    parser.add_argument('--locale')

    args = parser.parse_args()
    return Config(args)
