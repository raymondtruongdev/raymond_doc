#!/usr/bin/env bash
# Wrapper to convert Markdown to beautiful PDF
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
python3 "$DIR/md2pdf.py" "$@"
