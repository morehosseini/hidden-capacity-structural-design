# Changelog

## 1.3.1 — 28 October 2026

- Reconciled the Miller et al. reference to the 2013 publication and seven-author record used by the manuscript and Griffith University repository; updated every S1 reuse format.
- Distinguished organisation sensitivity from individual engineer accounts, and clarified the combined account-by-organisation predictor and band boundaries in Note S2.
- Aligned the README with the valid-ratio population, mean squared prediction error, figure-caption definitions and public-versus-request-only outputs.
- Documented the separate cleaning, uncertainty/robustness and prediction environments. Rebuilt both PDFs and refreshed checksums.
- Reported results, study-entry selection, CSV values in Tables S2–S7 and all six figure files are unchanged. No research analysis was rerun.
- The older v1.0.0 release remains available; use the main branch for this complete package.

## 1.3.0 — 28 October 2026

- Added the paper's three figures (PNG and vector PDF) in `figures/`, and a README that shows them with captions and a summary of the study.
- The README and the supplementary documents now describe the material for readers of the paper. Internal project names and draft version numbers were removed, as were drafting notes in the README, the changelog and Table S1.
- The two PDFs were rebuilt. Their footers show the document name, version and date, and the PDF build scripts read the version from the Markdown sources. Document versions now follow the package version.
- The v1.0.0 release notes and its PDF were updated to match.
- No data, table or analysis changed.

## 1.2.2 — 28 October 2026

The README, Note S2 and Table S1 cite the paper by its final title: *Strength to Spare, Deflection at the Limit: Governing Utilisation in 1.4 Million Structural Member Calculations*. Both PDFs were rebuilt. The repository keeps its address, https://github.com/morehosseini/hidden-capacity-structural-design, because the paper cites it.

## 1.2.1 — 27 October 2026

S2.6 states the de-duplication rule. The current key is applied after the validity filters, and the latest-created record is kept, with ties broken by sheet identifier. The key without the governing reference is the reported sensitivity. S2.6 also reports three checks:

- no member key had tied latest creation times;
- de-duplicating before the filters would keep 362 fewer records and change the mean by less than 0.0001;
- an explicit ISO 8601 parse recovers two creation times that had been left missing.

## 1.2.0 — 27 October 2026

S2.7 reports the uncertainty and robustness analyses, with Tables S4–S7 and CSV copies in `methods/`:

- organisation-cluster bootstrap intervals alongside the engineer-cluster interval, with and without the largest organisation (Table S4);
- strength- and deflection-governed means in the 46 shared templates at each group's own and at common template weights (Table S5);
- the deflection-governed share by band with template weights held fixed (Table S6);
- the full specification grid for the strength-governed, deflection-governed, headline and bearing-inclusive sets (Table S7).

The aggregation-sensitivity definitions are stated in full, including the four materials used for equal material weighting. The rows without the largest organisation omit engineer and group counts, as the data owner asked. No per-template result is released. The PDF build script now sets column widths for each table and renders superscripts the Arial font lacks.

## 1.1.1 — 27 October 2026

Added CSV copies of Supplementary Tables S2 and S3 in `methods/`, and a hosting statement in the README.

## 1.1.0 — 27 October 2026

Added Supplementary Note S2 (data and methods details). It holds the material moved out of the paper's methods section: supplied fields (Table S2), identifier and export scope notes, operator-confirmed check coverage and deflection-limit defaults, template classification and pseudonymisation, check-type mapping, governing-check storage order, Boolean-valued records, itemised disposition (Table S3), de-duplication tests, uncertainty and robustness procedures, prediction settings and workflow. Markdown source, PDF and build script supplied.

## 1.0.0 — 26 October 2026

Initial release of Supplementary Table S1, a 22-entry extended comparison. Eight entries appear in the paper's Table 1; three others are also acknowledged in its prose. Source and overlap qualifications are retained, and full references, a selection note and reuse formats are supplied.
