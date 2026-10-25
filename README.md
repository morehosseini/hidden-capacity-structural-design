# Paper A supplementary literature comparison

Version 1.0.0 · 26 October 2026

This folder contains the repository content accompanying the shortened Table 1 and Section 2.2 in Paper A, *Hidden Capacity in Everyday Structural Design*. Supplementary Table S1 preserves the complete 22-entry comparison; eight selected studies remain in the manuscript. The package contains literature summaries and provenance, independently of the empirical-analysis release.

## Read the supplement

- [Supplementary Table S1 PDF](supplementary_literature.pdf): self-contained table, source references, definitions, provenance and selection note.
- [Readable Markdown comparison](literature/table_S1_extended_evidence.md).
- [CSV](literature/table_S1_extended_evidence.csv) and [JSON](literature/table_S1_extended_evidence.json): the same 22 entries, including source, verification, overlap and placement fields.
- [References](literature/references.md).
- [Search and selection note](literature/search_and_selection_note.md).
- [PDF build script](scripts/build_literature_pdf.py).

The table is a curated comparison. Its entries measure different outcomes and may include related datasets. Neither their sample counts nor their outcome percentages should be pooled. Original sources should be cited when using their findings; this package does not replace those citations.

## Publication and citation status

This is local repository content prepared for GitHub upload. No remote GitHub destination, public release, archival DOI or journal acceptance is asserted. The manuscript refers to Supplementary Table S1 in the accompanying repository. Supply this PDF to reviewers alongside the manuscript.

When the Paper A repository is published, include this folder's contents, create a versioned release matching this package, archive that release with Zenodo or an equivalent persistent repository, and add its verified version DOI to the manuscript's Section 2.2 repository citation and this README. No DOI placeholder has been inserted into the scientific prose. Check the confirmed journal's supplementary-material requirements. Reconcile the separate, older empirical reproducibility bundle before describing it as current.

Suggested artifact title: *Extended comparison of structural utilisation and related design evidence*, version 1.0.0 (26 October 2026). Final author metadata and license can be supplied with the repository release. Source publications retain their own rights; this package supplies original summaries and source links rather than copies of publisher PDFs.

## Rebuild the PDF

Run `python scripts/build_literature_pdf.py` with Python, ReportLab and the Arial font family available. It reads the JSON (including full references) and the selection note in this package. File hashes are listed in `manifest_sha256.json`; regenerate them after an intentional content change.
