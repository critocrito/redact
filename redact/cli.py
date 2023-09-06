#!/usr/bin/env python3

import click
import sys
import tempfile
import logging

from . import AppEnvironment
from .redact import Redactor
from .actions import email_to_pdf, document_to_pdf
from .util import detect_file_type


@click.command()
@click.option("--redactions", type=click.File("r"),help="List of terms to redact.")
@click.option("--input", type=click.Path(exists=True), help="The file to redact.")
@click.option("--output", type=click.Path(), help="Output redacted file to this path.")
@click.option(
    "--log-file", type=click.Path(), help="Path to log file..", default="out.log"
)
@click.option(
    "--libreoffice",
    type=click.Path(),
    help="provide the path to the libreoffice (soffice) binary.",
    default="/usr/bin/libreoffice")
def main(redactions, input, output, log_file, libreoffice):
    env = AppEnvironment(libreoffice)

    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler(log_file)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    rootLogger.setLevel(logging.INFO)

    file_type = detect_file_type(input)

    if file_type is None:
        logging.error(f"Could not detect file type of {input}")
        sys.exit(1)

    redactions_re = []
    for line in redactions.readlines():
        redactions_re.append(line.strip())

    try:
        pdf_path = input

        # managing pre processing actions in this matter doesn't scale well
        # but it's good enough for two cases. I'm also accepting the fact that
        # a temp directory is created for each file, even if it doesn't need
        # it (i.e. PDF).
        with tempfile.TemporaryDirectory() as unique_tmpdir:
            if file_type == "mail":
                pdf_path = email_to_pdf(env, unique_tmpdir, input)

            if file_type == "document":
                pdf_path = document_to_pdf(env, unique_tmpdir, input)

            redactor = Redactor(pdf_path, output, input)
            redactor.redaction(redactions_re)

    except Exception as e:
        logging.error(f"Could not blacken {input}: {e}")


if __name__ == "__main__":
    main()
