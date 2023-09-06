class ProcessingException(Exception):
    "A data-related error occuring during file processing."
    pass


TIMEOUT = 3600  # seconds
CONVERT_RETRIES = 5


class AppEnvironment:
    def __init__(self, libreoffice_path):
        self.libreoffice_path = libreoffice_path
        self.timeout = TIMEOUT
        self.convert_retries = CONVERT_RETRIES

    def __repr__(self):
        return f"<AppEnvironment {self.libreoffice_path}>"
