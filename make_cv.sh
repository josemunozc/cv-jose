#!/bin/bash

set -eu

pandoc -s cv_en_john_doe.md -o cv_en_john_doe.docx
python md_to_tex.py cv_en_john_doe.md english
pdflatex cv_en_john_doe.tex
bibtex journal
bibtex conferences
bibtex misc
pdflatex cv_en_john_doe.tex
pdflatex cv_en_john_doe.tex