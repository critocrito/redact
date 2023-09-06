# Redact

> Automatically redact files based on a list of regular expressions.

**WARNING**: There is no guarentee that all occurences that require redaction are caught by this program. Make sure to manually verify the quality of the redactions.

## Installation

Install [Poetry](https://python-poetry.org/docs/#installation) to manage depencies of `redact`. Once installed setup the dependencies:

``` sh
poetry install
```

`redact` requires additional software to be available on the host system:

- `libmagic` to detect the file type.
- `wkhtmltopdf` to convert Outlook messages to PDF.
- `libreoffice` to convert documents to PDF.

Test that the application works:

``` sh
poetry run redact --help
```

## Usage

`redact` takes a file containing a list of strings to redact and a single PDF file as input and outputs a redacted version. Documents that are not PDF's are converted to a PDF first and a redacted version of the PDF is written as output. Currently `redact` understands the following additional file types:

- Wordprocessing documents
- Outlook message files

To invoke `redact` run:

``` sh
echo <<EOF >> redactions.txt
Alice
Bob
(Jane|Joe) Doe
EOF

poetry run redact \
  --redactions redactions.txt \    # A text file with one regular expression per line.
  --input path/to/file.doc \       # The path to the input file to redact.
  --output path/to/file.doc.pdf \  # The path to the output file containing the redactions.
```

There are the following additional command options:

- `--libreoffice`: specify the path to the Libreoffice binary. The default is `/usr/bin/libreoffice` but on my macOS I have to set it to `/opt/homebrew/bin/soffice`.
- `--log-file`: append the log output to this file. It defaults to `out.log`.

### Redact files in bulk

To redact files in bulk and in parallel I wrap the invocation to `redact` in a shell script.


``` sh
cat <<EOF >> redact.sh
#!/usr/bin/env sh

set -Eeuo pipefail

INPUT="$1"

DIR=$(dirname "$INPUT")
OUTDIR="redacted/$DIR"

FILE=$(basename "$INPUT")
OUTFILE="$OUTDIR/$FILE"

mkdir -p "$OUTDIR"

poetry run redact \
       --redactions redactions.txt \
       --input "$INPUT" \
       --output "$OUTFILE" \
       --libreoffice /opt/homebrew/bin/soffice
EOF

chmod +x redact.sh

find path/to/folder -type f -print0 | xargs -0 -n1 -P8 ./redact.sh
```

### Extracting stats from the log file

The log file can be used to produce a list of files that were processed, failed to process or to count the number of redactions.

``` sh
# Count the number of redactions
sed -n 's/.*Successfully redacted \([0-9]*\) areas./\1/p' out.log > stats.txt

# Count the number of files that failed
grep ERROR out.log | wc-l

# List of redacted files
rg "Succesfully redacted" out.log | ggrep -oP ".*\/Users\/christo\/documents(.*)$"

# List files with no redactions
rg "no redactions" out.log | sed -e 's/.*\[INFO \] \/Users\/christo\/documents\/\(.*\) had no redactions.$/\1/' | sort | uniq > unredacted.txt
```

To compare the file tree between un-redacted and redacted files:

``` sh
find path/to/files -type f > all-files.txt
find path/to/redacted-files -type f > redacted-files.txt

comm -13 all-files.txt redacted-files.txt > files-missing.txt
comm -23 all-files.txt redacted-files.txt > processed-files.txt 
```

