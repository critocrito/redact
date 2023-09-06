import magic
from pathlib import Path
from pantomime import normalize_mimetype

from . import PDF_MIME_TYPES, DOCUMENT_MIME_TYPES, MAIL_MIME_TYPES


MAGIC = magic.Magic(mime=True)


def mime_types(source_mime_types):
    mime_types = [normalize_mimetype(m, default=None) for m in source_mime_types]
    mime_types = [m for m in mime_types if m is not None]
    return mime_types


def ensure_path(file_path):
    if file_path is None or isinstance(file_path, Path):
        return file_path
    return Path(file_path).resolve()


def detect_file_type(file_name):
    input_path = ensure_path(file_name)

    pdf_mime_types = mime_types(PDF_MIME_TYPES)
    document_mime_types = mime_types(DOCUMENT_MIME_TYPES)
    mail_mime_types = mime_types(MAIL_MIME_TYPES)

    file_mime_type = MAGIC.from_file(input_path.as_posix())

    if file_mime_type in pdf_mime_types:
        return "pdf"

    if file_mime_type in mail_mime_types:
        return "mail"

    if file_mime_type in document_mime_types:
        return "document"

    return None
