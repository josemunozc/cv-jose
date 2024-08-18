#!/bin/bash

set -eu

pandoc -s resume.md -o resume.docx
python md_to_tex.py resume.md english
pdflatex resume.tex
bibtex journal
bibtex conferences
bibtex misc
pdflatex resume.tex
pdflatex resume.tex

# Create a separate file with list of references in markdown
# these will be added to the base resume using cat
pandoc -t markdown_strict --citeproc pandoc-bib.md -o publications.md --bibliography publications.bib

# using index.md to publish in GitHub
cat resume.md > index.md
cat publications.md >> index.md

# do some cleaning
rm -f *.bcf *.blg *.bbl *.aux *.log
