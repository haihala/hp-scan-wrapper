from __future__ import annotations

import re

from config import Config

email_regex = re.compile(r'^\S+@\S+\.\S+$')


def ask_if_done(config: Config) -> bool:
    yes = config.get_translation('yes')
    no = config.get_translation('no')
    while True:
        try:
            choice = input(
                config.get_translation('another_page_prompt')
            ).lower()[0]
            if choice in [yes, no]:
                return choice == no
        except:
            config.print('retry_input')


def ask_presentation(config: Config) -> tuple[bool, bool]:
    config.print('presentation_prompt')

    while True:
        str_choice = input(config.get_translation('presentation_input'))
        try:
            parsed_choice = int(str_choice[0])
            if parsed_choice == 1:
                return True, False
            elif parsed_choice == 2:
                return False, True
            elif parsed_choice == 3:
                return True, True
            elif parsed_choice == 4:
                config.print('quitting')
                return False, False
        except:
            config.print('retry_input')


def ask_email(config: Config) -> str:
    config.print('email_prompt_header')
    for index, email in enumerate(config.used_emails):
        print(config.get_translation('email_prompt_row').format(index+1, email))

    while True:
        choice = input(config.get_translation('email_input'))
        if choice.isdigit():
            # Number, user wants to reuse an email
            number = int(choice)
            if number <= len(config.used_emails):
                return config.used_emails[number-1]

        if email_regex.match(choice):
            config.used_emails.append(choice)
            return choice

        config.print('retry_input')
