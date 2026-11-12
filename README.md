# CV

`cv.tex` is the whole CV: layout, text and styles in one LaTeX file. It needs **XeLaTeX** (or Tectonic), because it loads the bundled fonts from `fonts/` with `fontspec`.

## Build

With TeX Live or MiKTeX:

```bash
xelatex cv.tex
xelatex cv.tex   # second run fills in the "1 / 2" page totals
```

or `latexmk -xelatex cv.tex`, or with [Tectonic](https://tectonic-typesetting.github.io/) (one binary, fetches packages itself):

```bash
tectonic cv.tex
```

This writes `cv.pdf`.

Packages used: fontspec, xcolor, tikz (svg.path), tcolorbox, enumitem, ulem, xstring, fancyhdr, lastpage, hyperref, geometry, graphicx, calc.

## ATS / text extraction

The PDF is built so its text extracts cleanly (checked with pypdf, pdfminer and poppler's pdftotext):

- Contact icons are drawn as vector shapes (`\iconmail` etc., Font Awesome Free paths), not font glyphs, so they add no stray characters to the extracted text.
- Section headings are letterspaced with the PDF `Tc` operator, so they extract as `EXPERIENCE` rather than `E X P E R I E N C E`. The spacing (`\cvtrack`, 0.7bp) must stay under 0.84bp: above that, pdfminer, which many resume parsers use, reads the gaps as spaces.
- The link arrows and bullet dots are drawn, not typed, so no `↗` or `•` characters end up in the extracted text.
- Apostrophes stay straight (`'`), matching what people type in keyword searches. TeX's `--` shortcut is off, so type en dashes directly: `2025 – 2029`.
- Inter kerns `7.` and `7,` so tightly that some parsers read a space (`17 .6`). Put `\nk` between them, as in `17\nk.6/20`.

To check after editing:

```bash
pip install pypdf pdfminer.six
python scripts/ats_check.py cv.pdf
```

It also uses poppler's `pdftotext` when it's installed.

## Editing

- Page 1 (summary, education, experience) and page 2 (projects, skills) are split by `\newpage`, marked with comments.
- Each block is an `entry` environment: `\begin{entry}{logo.png}{Title}{Dates} ... \end{entry}`. Leave the logo argument empty (`{}`) for a box without an icon. Use `\sub{...}` for grey sub-lines and `itemize` for bullets.
- `\link{url}{text}` makes an underlined accent link with the ↗ arrow; `\plainlink` is the same without the arrow (mail, phone). `\sep` is the `·` separator.
- Colors are `\definecolor` lines near the top; `accent` is the blue.
- Footer text is set in the `\fancyfoot` lines near the top (including the "Last updated" date).
- LaTeX does not clip overflow: if a page gets too long, content moves to a new page. Check that the PDF is still two pages after adding text.

## Files

- `cv.tex` - the CV
- `icons/` - project and organisation logos, taken from each project's repo or site
- `fonts/` - Inter (Regular, SemiBold, Bold) and Liberation Serif Bold (both SIL Open Font License), bundled so the PDF looks the same everywhere
