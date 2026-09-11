I have one or more PDF files that need to be converted to Markdown (.md, same base filename as the PDF). These are technical/protocol documents containing tables with irregular structure — merged cells, rowspan/colspan, blank cells — so accuracy matters more than speed.

  Conversion process:
  1. Read the PDF in full (all pages).
  2. Reproduce the document structure in Markdown: headings, paragraphs, lists, bold/italic emphasis, footnotes, code blocks, formulas — matching the source as closely as Markdown allows.
  3. For tables:
     - Regular tables (no merged cells) → standard Markdown pipe tables (| a | b |).
     - Irregular tables (any rowspan/colspan — e.g. one value or ID spanning several rows, a header cell spanning several columns) → use raw HTML <table> with explicit rowspan/colspan attributes. Do not flatten these into pipe tables — that silently duplicates or drops data.
     - Preserve every cell value verbatim: numbers, ranges, hex/binary codes, units, bit-field names and their meanings.
  4. Do not silently "fix" the source. If the PDF has an apparent typo, inconsistent spacing, or odd formatting (e.g. "chat" instead of "char", a malformed date like "018.08.2026"), carry it through unchanged in the .md. The goal is a faithful transcription, not a corrected one.
  5. Preserve document metadata exactly: title, version number, date, interface/protocol names.
  6. Write the result to <same-basename>.md next to the source PDF.
  7. create a separate markdown per page
  8. In the add concatanete those markdowns into single document ( if some table, or formula or other such element was split accorss pages, then merge them)

  After conversion — verify it:
  1. Re-read both the PDF and the newly written .md in full.
  2. Compare them section by section, especially the irregular tables — check that rowspan/colspan cells map correctly and no values were duplicated, dropped, or shifted to the wrong row/column.
  3. Check every data value verbatim against step 3 above.
  4. If there are multiple related PDFs (e.g. different versions of the same document), note version-specific differences (a value/option present in one version but not another) and confirm the .md reflects its own version, not another's.

  Output: After conversion, give a concise report: what was converted, any tables that needed HTML (with rowspan/colspan) vs. plain Markdown, and the result of the verification pass — matches confirmed, and any discrepancies found (file, location, what's wrong, what it should be). If everything checks out after the fix, say so clearly.

  wait for instauctions