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

Packages used: fontspec, fontawesome5, xcolor, tikz, tcolorbox, enumitem, ulem, fancyhdr, lastpage, hyperref, geometry, graphicx, calc.

## Editing

- Page 1 (summary, education, experience) and page 2 (projects, skills) are split by `\newpage`, marked with comments.
- Each block is an `entry` environment: `\begin{entry}{logo.png}{Title}{Dates} ... \end{entry}`. Leave the logo argument empty (`{}`) for a box without an icon. Use `\sub{...}` for grey sub-lines and `itemize` for bullets.
- `\link{url}{text}` makes an underlined accent link with the ↗ arrow; `\plainlink` is the same without the arrow (mail, phone). `\sep` is the `·` separator.
- Colors are `\definecolor` lines near the top; `accent` is the blue.
- Footer text is set in the `\fancyfoot` lines near the top (including the "Last updated" date).
- Contact icons come from the `fontawesome5` package.
- LaTeX does not clip overflow: if a page gets too long, content moves to a new page. Check that the PDF is still two pages after adding text.

## Files

- `cv.tex` - the CV
- `icons/` - project and organisation logos, taken from each project's repo or site
- `fonts/` - Inter (Regular, SemiBold, Bold) and Liberation Serif Bold (both SIL Open Font License), bundled so the PDF looks the same everywhere
