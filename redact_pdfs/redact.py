import logging
import fitz
import re
import click
import sys
import os
import pathlib
import subprocess
import tempfile


TIMEOUT = 3600  # seconds
CONVERT_RETRIES = 5


class ProcessingException(Exception):
    "A data-related error occuring during file processing."
    pass


class Redactor:
    @staticmethod
    def get_sensitive_data(lines, redactions):
        """Function to get all the lines"""
        for line in lines:
            for name in redactions:
                if re.search(name, line, re.IGNORECASE):
                    search = re.search(name, line, re.IGNORECASE)

                    yield search.group(0)

    def __init__(self, input, output):
        self.input = input
        self.output = output

    def redaction(self, redactions):
        """main redactor code"""
        doc = fitz.open(self.input)
        count = 0

        for page in doc:
            # _wrapContents is needed for fixing
            # alignment issues with rect boxes in some
            # cases where there is alignment issue
            page.wrap_contents()

            # getting the rect boxes which consists the matching email regex
            sensitive = self.get_sensitive_data(
                page.get_text("text").split("\n"), redactions
            )

            for data in sensitive:
                areas = page.search_for(data)

                # drawing outline over sensitive datas
                [page.add_redact_annot(area, fill=(0, 0, 0)) for area in areas]

                count += 1

            # applying the redaction
            page.apply_redactions()

        # saving it to a new pdf
        doc.save(self.output)

        if count > 0:
            logging.info(f"Successfully redacted {count} areas in {self.input}.")
        else:
            logging.info(f"{self.input} had no redactions.")


def document_to_pdf(unique_tmpdir, file_path, timeout=TIMEOUT):
    """Converts an office document to PDF."""
    logging.info("Converting [%s] to PDF", file_path)

    pdf_output_dir = os.path.join(unique_tmpdir, "out")
    libreoffice_profile_dir = os.path.join(unique_tmpdir, "profile")
    pathlib.Path(pdf_output_dir).mkdir(parents=True)
    pathlib.Path(libreoffice_profile_dir).mkdir(parents=True)

    cmd = [
        # "/usr/bin/libreoffice",
        "/opt/homebrew/bin/soffice",
        '"-env:UserInstallation=file://{}"'.format(libreoffice_profile_dir),
        "--nologo",
        "--headless",
        "--nocrashreport",
        "--nodefault",
        "--norestore",
        "--nolockcheck",
        "--invisible",
        "--convert-to",
        "pdf",
        "--outdir",
        pdf_output_dir,
        file_path,
    ]

    try:
        for attempt in range(1, CONVERT_RETRIES):
            logging.info(
                f"Starting LibreOffice: %s with timeout %s attempt #{attempt}/{CONVERT_RETRIES}",
                cmd,
                timeout,
            )
            try:
                subprocess.run(cmd, timeout=timeout, check=True)
            except Exception as e:
                logging.info(
                    f"Could not be converted to PDF (attempt {attempt}/{CONVERT_RETRIES}): {e}"
                )
                continue

            for file_name in os.listdir(pdf_output_dir):
                if not file_name.endswith(".pdf"):
                    continue
                out_file = os.path.join(pdf_output_dir, file_name)
                if os.stat(out_file).st_size == 0:
                    continue
                logging.info(f"Successfully converted {out_file}")
                return out_file
        raise ProcessingException(
            f"Could not be converted to PDF (attempt #{attempt}/{CONVERT_RETRIES})"
        )
    except Exception as e:
        raise ProcessingException("Could not be converted to PDF") from e


@click.command()
@click.option("--redactions", type=click.File("r"), help="List of terms to redact.")
@click.option("--input", type=click.Path(exists=True), help="The file to redact.")
@click.option("--output", type=click.Path(), help="Output redacted file to this path.")
@click.option(
    "--log-file", type=click.Path(), help="Path to log file..", default="out.log"
)
def main(redactions, input, output, log_file):
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler(log_file)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    rootLogger.setLevel(logging.DEBUG)

    redactions_re = []
    for line in redactions.readlines():
        redactions_re.append(line.strip())

    with tempfile.TemporaryDirectory() as unique_tmpdir:
        # TODO - write to logs the case in which the context manager can't delete these dirs
        pdf_path = document_to_pdf(unique_tmpdir, input)

        redactor = Redactor(
            pdf_path,
            output,
        )

        redactor.redaction(redactions_re)


if __name__ == "__main__":
    main()
