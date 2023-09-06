import logging
import os
import pathlib
import subprocess
import extract_msg

from . import ProcessingException

TIMEOUT = 3600  # seconds
CONVERT_RETRIES = 5


def document_to_pdf(unique_tmpdir, file_path, timeout=TIMEOUT):
    """Converts an office document to PDF."""
    logging.debug("Converting [%s] to PDF", file_path)

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
            logging.debug(
                f"Starting LibreOffice: %s with timeout %s attempt #{attempt}/{CONVERT_RETRIES}",
                cmd,
                timeout,
            )
            try:
                subprocess.run(cmd, timeout=timeout, check=True)
            except Exception as e:
                logging.debug(
                    f"Could not be converted to PDF (attempt {attempt}/{CONVERT_RETRIES}): {e}"
                )
                continue

            for file_name in os.listdir(pdf_output_dir):
                if not file_name.endswith(".pdf"):
                    continue
                out_file = os.path.join(pdf_output_dir, file_name)
                if os.stat(out_file).st_size == 0:
                    continue
                logging.debug(f"Successfully converted {out_file}")
                return out_file
        raise ProcessingException(
            f"Could not be converted to PDF (attempt #{attempt}/{CONVERT_RETRIES})"
        )
    except Exception as e:
        raise ProcessingException("Could not be converted to PDF") from e


def email_to_pdf(outdir, file_path):
    """Converts a outlook email message to a pdf."""
    out_file = os.path.join(outdir, "out", "message.pdf")
    msg = extract_msg.openMsg(file_path)
    msg.save(pdf=True, customPath=outdir, customFilename="out")

    return out_file
