import logging
import fitz
import re


class Redactor:
    @staticmethod
    def get_sensitive_data(lines, redactions):
        """Function to get all the lines"""
        for line in lines:
            for name in redactions:
                if re.search(name, line, re.IGNORECASE):
                    search = re.search(name, line, re.IGNORECASE)

                    yield search.group(0)

    def __init__(self, input, output, original):
        self.input = input
        self.output = output
        self.original = original

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
            logging.info(f"Successfully redacted {count} areas in {self.original}.")
        else:
            logging.info(f"{self.original} had no redactions.")
