import logging
import fitz
import re
import click
import sys


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

            # applying the redaction
            page.apply_redactions()

        # saving it to a new pdf
        doc.save(self.output)
        logging.info(f"Successfully redacted {self.input} to {self.output}")


@click.command()
@click.option("--redactions", type=click.File("r"), help="List of terms to redact.")
@click.option("--input", type=click.Path(exists=True), help="The file to redact.")
@click.option("--output", type=click.Path(), help="Output redacted file to this path.")
def main(redactions, input, output):
    logging.basicConfig(stream=sys.stdout)

    redactions_re = []
    for line in redactions.readlines():
        redactions_re.append(line.strip())

    redactor = Redactor(
        input,
        output,
    )

    redactor.redaction(redactions_re)


if __name__ == "__main__":
    main()
