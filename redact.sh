#!/usr/bin/env sh

set -Eeuo pipefail

INPUT="$1"

DIR=$(dirname "$INPUT")
OUTDIR="redacted/$DIR"

FILE=$(basename "$INPUT")
OUTFILE="$OUTDIR/$FILE"

mkdir -p "$OUTDIR"

poetry run redact_pdfs/redact.py --redactions redactions.txt --input "$INPUT" --output "$OUTFILE"
