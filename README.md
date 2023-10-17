<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL-3.0 License][license-shield]][license-url]


<br />
<div align="center">
  <h3 align="center">Redact</h3>

  <p align="center">
    Redact files in bulk based on a list of regular expressions.
    <br />
    <a href="https://github.com/critocrito/redact/issues">Report Bug</a>
    ·
    <a href="https://github.com/critocrito/redact/issues">Request Feature</a>
  </p>
</div>


<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


## About The Project

Automatically redact files based on a list of regular expressions.

**WARNING**: There is no guarentee that all occurences that require redaction are caught by this program. Make sure to manually verify the quality of the redactions.

This code was developed to help with network analyses for various investigations that took place at [Der SPIEGEL](https://spiegel.de) and [Paper Trail Media](https://papertrailmedia.de).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

The project uses [Poetry](https://python-poetry.org) to manage python dependencies. To install see the [Poetry documentation](https://python-poetry.org/docs/#installation) for all options. To use the quick installer provided by Poetry run:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

`redact` requires additional software to be available on the host system:

- `libmagic` to detect the file type.
- `wkhtmltopdf` to convert Outlook messages to PDF.
- `libreoffice` to convert documents to PDF.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/critocrito/redact.git
   ```
2. Install the python dependencies
   ```sh
   poetry install
   ```
3. Test that the application works:
   ``` sh
   poetry run redact --help
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


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

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## License

Distributed under the GPL-3 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contact

Your Name - [@christo_buschek](https://twitter.com/christo_buschek) - christo.buschek@proton.me.com

Project Link: [https://github.com/critocrito/redact](https://github.com/critocrito/redact)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[contributors-shield]: https://img.shields.io/github/contributors/critocrito/redact.svg?style=for-the-badge
[contributors-url]: https://github.com/critocrito/redact/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/critocrito/redact.svg?style=for-the-badge
[forks-url]: https://github.com/critocrito/redact/network/members
[stars-shield]: https://img.shields.io/github/stars/critocrito/redact.svg?style=for-the-badge
[stars-url]: https://github.com/critocrito/redact/stargazers
[issues-shield]: https://img.shields.io/github/issues/critocrito/redact.svg?style=for-the-badge
[issues-url]: https://github.com/critocrito/redact/issues
[license-shield]: https://img.shields.io/github/license/critocrito/redact.svg?style=for-the-badge
[license-url]: https://github.com/critocrito/redact/blob/master/LICENSE.txt
