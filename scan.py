from __future__ import annotations

from datetime import datetime
import smtplib
import subprocess
import os.path as ospath
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from config import (
    Config,
    parse_args,
)
from user_input import (
    ask_email,
    ask_if_done,
    ask_presentation,
)


def main():
    config = parse_args()

    files, folder, email = scan(config)

    if email:
        send_email(config, files)

    if folder:
        open_folder(config)

    config.write_config()


def scan(config: Config) -> list[str]:
    # Perform scanning, return list of paths for new files
    files = []
    while True:
        new_file = scan_page(config)
        files.append(new_file)

        if ask_if_done(config):
            break

    presentation = ask_presentation(config)
    return files, *presentation


def scan_page(config: Config) -> str:
    # Scans a page, returns the path
    config.print('scan_page')
    file_name = datetime.now().strftime(config.date_format_string)
    path = ospath.join(config.target_dir, file_name)
    handle = subprocess.Popen(
        f'hp-scan --file="{path}"',
        shell=True,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    handle.communicate(input=f'{config.device}\n'.encode())
    handle.wait()
    return path


def open_folder(config: Config) -> None:
    subprocess.Popen(
        f'{config.file_explorer} {config.target_dir}',
        shell=True,
        start_new_session=True,
    ).wait()


def send_email(config: Config, files: list[str]) -> None:
    recipient = ask_email(config)

    session = start_session(config)

    session.sendmail(
        config.smtp_sender,
        recipient,
        format_message(
            config,
            files,
            recipient,
        ),
    )
    session.quit()


def start_session(config: Config) -> smtplib.SMTP:
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(config.smtp_sender, config.smtp_password)
    return session


def format_message(config: Config, files: list[str], recipient: str) -> str:
    message = MIMEMultipart()

    message["From"] = config.smtp_sender
    message['To'] = recipient
    message['Subject'] = config.get_translation('email_subject')

    for file_path in files:
        file_name = ospath.split(file_path)[-1]
        with open(file_path, 'rb') as handle:
            obj = MIMEBase('application', 'octet-stream')
            obj.set_payload(handle.read())
            encoders.encode_base64(obj)
            obj.add_header('Content-Disposition',
                           f'attachment; filename={file_name}')
            message.attach(obj)

    return message.as_string()


if __name__ == '__main__':
    main()
