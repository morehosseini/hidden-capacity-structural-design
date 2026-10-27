# Supplementary Note S2. Data and methods details

Version 1.3.1 · 28 October 2026

This note accompanies Section 3 (Data and methods) of the paper *Strength to Spare, Deflection at the Limit: Governing Utilisation in 1.4 Million Structural Member Calculations*. It records the field definitions, platform behaviour confirmed by the operator, classification and storage rules, de-duplication tests and model settings that the main text summarises. All counts refer to the Calcs.com export analysed in the paper. The underlying calculation records are held by Calcs.com and are not part of this repository; access is described in the paper's Data availability statement.

## S2.1 Supplied fields and identifiers

The raw export contained 2,844,654 calculation-sheet records from paid accounts, created between January 2024 and June 2025, with the twelve fields in Table S2.

**Table S2. Supplied platform fields and the role of each in the analysis.**

| Field | Role in the analysis |
| --- | --- |
| sheet_template_id | Template identifier retained for provenance. |
| sheet_template_code | Template classification and de-duplication key; pseudonymised where the code carried a customer name (S2.3). |
| sheet_template_version | Template-version provenance. |
| sheet_created_at | Time the sheet was created; chronology and de-duplication ordering. |
| sheet_id | Calculation-sheet identifier; one row per sheet. |
| sheet_name | User-assigned member label, used only inside the de-duplication key; contents not analysed or reported. |
| summary_check_value | Governing utilisation of the sheet, parsed to D/C where valid. |
| summary_check_reference_id | Identifier of the governing check to which the value refers. |
| user_id | Pseudonymous user account used for engineer-account grouping. |
| project_id | Pseudonymous project grouping. |
| organisation_id | Pseudonymous organisation grouping. |
| payment_status | Snapshot provenance; all records are from paid accounts. |

The timestamp recorded when a sheet was created. The operator confirmed that the time of the last edit is held in a separate field that was not part of this export.

The headline population contained 3,073 distinct user identifiers and 1,735 organisation identifiers. Largest-organisation sensitivity refers to an organisation_id group, rather than to an individual user_id account. Each user identifier was treated as an engineer account; an account is not independently verified as a distinct professional engineer. Every project belonged to one organisation at the time of export, while 21 of the 3,073 user identifiers occurred under more than one organisation in the headline population. The operator attributed such cases mainly to support access, changes of membership or moved projects. Some projects involved more than one engineer, so projects and engineer accounts did not form a strictly nested hierarchy.

Australian, US and Canadian design-standard families were represented in the calculators. The export contained no project-location field, so the standard family identifies the calculator's design basis rather than the country of the project or user. The export also contained no three-dimensional finite-element models, member geometry, section catalogue options, quantities, cost, embodied carbon or project outcome data.

## S2.2 Check coverage and deflection limits

The platform operator confirmed three features of check coverage. Connections are checked in separate calculators from the members they join. Vibration checks are a newer platform feature and were absent from this export. Fire resistance is assessed by the engineer outside the platform.

Deflection utilisation is measured against a limit that each calculator supplies as a default from the local standard. According to the operator, the defaults follow AS 1170 in Australian calculators, the IBC and IRC deflection tables in US calculators, and NBCC Part 9 with CSA O86 in Canadian calculators. Engineers can override the default, including by combining a span-ratio limit with an absolute limit in millimetres. The limit applied to each calculation was not part of the export.

## S2.3 Template classification and pseudonymisation

A lookup of 179 template codes assigned each code a material class (timber, steel, concrete, cold-formed steel, masonry or FRP-concrete) and a member type (beam, column, wall, connection, slab, truss and related types), or placed it outside the structural scope. Templates outside that scope, including a group of proprietary specialty calculators and exploratory aluminium templates, were excluded. Classification was applied once, in the cleaning stage, and every downstream statistic used the classified output.

Twenty-three template codes carried the name of a platform customer, an end customer or a component vendor. At the data owner's request, these codes were pseudonymised in every released artefact. The renaming was one-to-one and was applied after classification, so material and member-type labels, the de-duplication key and every reported statistic were unchanged. The crosswalk to the original codes is not released, and no statistic is reported for any individual template.

## S2.4 Check-type mapping

The stored value was heterogeneous: its meaning was carried by an accompanying reference identifier, of which about 752 distinct values occurred. Each reference was mapped to a check type (ULS strength, SLS deflection, bearing or geotechnical, factor of safety, geometric limit, or unknown) and flagged according to whether it belonged to the strength, deflection and bearing classes analysed in the paper. The mapping combined 78 hand-verified overrides with an ordered pattern fallback that resolved deflection before strength and placed geometric references last. A coverage gate required at least 99% of candidate records to receive a check type. Coverage reached 99.36% after the most frequent unresolved references were inspected and added to the overrides. Coverage measures assignment rather than accuracy.

The operator described every numeric check as a ratio for which a value of 1 or less passes. The 30,831 records whose reference was a factor of safety, a geometric limit or unclassified were therefore governing checks of another kind rather than raw dimensions; 92.7% of their values lay between 0 and 1. They were excluded by check type.

## S2.5 Governing-check storage and excluded records

The operator confirmed in writing that the stored reference identifies the governing check of each calculation sheet and that the stored value is the utilisation of that check; the reported check is not fixed by template. The valid-ratio product contained 1,454,574 rows and the same number of distinct sheet identifiers.

Each check returns either a number, for which 1 or less passes, or a Boolean. The sheet stores its worst result in a fixed order documented by the operator: a solve error first, then a false value, then the highest number, then a true value. Where checks tie, the first in sheet order is recorded. A false value therefore replaces any numeric utilisation on the same sheet, and a true value is stored only when no check on the sheet is numeric. Because only one result is stored, a sheet governed by a strength check carries no deflection information, and vice versa.

Of the 30,721 structural-template records that stored a Boolean value, the 19,156 true-valued records carried no utilisation. Of these, 94.3% came from calculators with no design check: one distributes forces in a bolt group and checks nothing, and the portal-frame calculators check only that the inputs are valid. The 11,565 false-valued records were sheets on which a Boolean check failed, and the operator reported that most are not capacity failures. Among the records whose references the operator described, which made up half of the total, 85% concerned depth limits set by the engineer, design codes or load cases that a calculator does not support, detailing rules and warnings; 15% were strength failures reported as Booleans. Boolean-valued records were excluded without being counted as failed designs. Passing the checks that a template records does not by itself show that the whole design complied with the applicable code or was accepted as final.

**Table S3. Itemised disposition of structural-template records.**

| Disposition | n | % of structural | Note |
| --- | ---: | ---: | --- |
| Valid governing utilisation | 1,454,574 | 89.99 | 0 < D/C ≤ 1 on a strength, deflection or bearing check; enters the analysis. |
| Over unity | 82,524 | 5.11 | Numeric governing utilisation above unity; summarised by check type in Section 4.6 of the paper. |
| Other governing check | 30,831 | 1.91 | Reference is a factor of safety, a geometric limit or unclassified; outside the classes analysed (S2.4). |
| Boolean-valued summary record | 30,721 | 1.90 | True (19,156): no numeric check on the sheet. False (11,565): a Boolean check failed. Not counted as failed designs (S2.5). |
| Solve error | 14,441 | 0.89 | Stored value is an error: not a number, or infinite. |
| Empty | 2,246 | 0.14 | No stored summary value. |
| Non-positive | 1,109 | 0.07 | Parsed value ≤ 0. |
| Total structural-template records | 1,616,446 | 100.00 | |

The Boolean-valued row is excluded because it carries no numeric ratio; it is not a count of failed designs.

## S2.6 Unit of observation and de-duplication

The operator confirmed that one sheet always represents a single member. The exceptions are the calculators for portal frames and trusses, which combine several members in one sheet. They are analysis-only: they evaluate no member check, store no utilisation and contributed no records to the analysis set.

Engineers iterate, so a project accumulates repeated calculations of the same member, and the platform has no flag that marks a calculation as final. De-duplication kept the most recently created record for each combination of project, template, governing reference and sheet name. The operator identified the user-assigned sheet name as the best available indicator of a member's purpose, and including it kept distinct named members apart: on a 250,000-record test, a coarser key without it retained 23,604 strength-governed records against 34,581 with it.

Shared names were rare. Of the 1,427,472 valid strength and deflection records, 98.1% had a combination of project, template and sheet name that no other record shared. Where a name was shared, the records resembled iterations of one member: 96.5% of the shared-name groups came from a single engineer, and in 63.0% all records were created within one hour. Because the key includes the governing reference, a member whose governing check changed between iterations can appear more than once, as happened in 40.2% of the shared-name groups. Removing the reference from the key reduced the set by 4,712 records (0.3%) and changed the mean by less than 0.001; this key is the reported sensitivity. De-duplication was applied after the validity filters and kept the most recently created record, with ties broken by sheet identifier. No member key had two records sharing the latest creation time, so the tie rule changed no selection. Applying de-duplication before the validity filters instead would have kept 362 fewer records and changed the mean by less than 0.0001. Creation times were read in ISO 8601 format, which recovered two times that an inferred format had left missing; both belonged to keys with a single record. A recalculation saved under a different sheet name can be retained more than once.

Sheet names can contain personal information. They were held internally under the operator's conditions, used only inside the de-duplication key, and never analysed, reported or released.

## S2.7 Uncertainty and robustness

Uncertainty for the headline mean used a cluster bootstrap with 1,000 replicates and seed 20260910. Each replicate resampled whole clusters with replacement and recomputed the record-weighted mean as total utilisation divided by the number of records; the interval runs from the 2.5th to the 97.5th percentile of the replicates. Engineer accounts were the primary clusters. Because projects nest within organisations and one organisation supplied about half of the records, the bootstrap was repeated with organisations as clusters (Table S4). The organisation interval is more than twice as wide as the engineer interval and extends further above the mean than below it, because a replicate can omit or repeat the largest organisation, whose mean is below that of the other organisations. Both intervals are conditional on the observed platform population.

**Table S4. Bootstrap 95% intervals for the record-weighted governing mean.**

| Population | Resampling unit | Mean | 95% interval | Width relative to independent records |
| --- | --- | ---: | ---: | ---: |
| Headline set | Records (independent) | 0.5471 | 0.5467–0.5476 | 1.0 |
| Headline set | Engineer accounts | 0.5471 | 0.5380–0.5576 | 22.3 |
| Headline set | Organisations | 0.5471 | 0.5355–0.5812 | 51.9 |
| Without the largest organisation | Records (independent) | 0.5657 | 0.5651–0.5663 | 1.0 |
| Without the largest organisation | Engineer accounts | 0.5657 | 0.5498–0.5805 | 24.5 |
| Without the largest organisation | Organisations | 0.5657 | 0.5446–0.5844 | 31.7 |

Aggregation sensitivity recomputed the governing mean with each record, project (85,581 projects), engineer account (3,073), material group or limit-state group weighted equally. Equal material weighting averaged the means of timber, steel, concrete and cold-formed steel; adding the six FRP-concrete records as a fifth group would raise it from 0.5507 to 0.6138. Equal limit-state weighting averaged the strength-governed and deflection-governed means. A largest-organisation sensitivity repeated the main analyses with and without the organisation that supplied about half of the records.

A template-coverage decomposition compared templates observed in both governing groups with those observed in only one. Within the 46 shared templates the two groups were then compared at common template weights (Table S5). With each group's own records as weights, the strength-governed mean weights templates by their strength-governed records and the deflection-governed mean by their deflection-governed records, so the two means do not weight the templates in the same way. Common weights apply the same template weights to both means: either each template's records in both groups together, or equal weight per template. The deflection-governed mean was the higher of the two in 40 of the 46 templates, in 33 of the 36 templates with at least 30 records in each group, and in 41 of 46 without the largest organisation. These comparisons describe the recorded groups; they are not causal adjustments.

**Table S5. Strength- and deflection-governed means in templates observed in both governing groups, by template weighting.**

| Population | Template weights | Templates | Strength mean | Deflection mean | Difference |
| --- | --- | ---: | ---: | ---: | ---: |
| Headline set | Each group’s own records | 46 | 0.4705 | 0.6259 | 0.1554 |
| Headline set | Common: records in both groups | 46 | 0.4493 | 0.6412 | 0.1919 |
| Headline set | Common: equal per template | 46 | 0.4972 | 0.6617 | 0.1645 |
| Headline set, templates with ≥ 30 records in each group | Each group’s own records | 36 | 0.4704 | 0.6259 | 0.1555 |
| Headline set, templates with ≥ 30 records in each group | Common: records in both groups | 36 | 0.4492 | 0.6412 | 0.1920 |
| Headline set, templates with ≥ 30 records in each group | Common: equal per template | 36 | 0.4897 | 0.6669 | 0.1772 |
| Without the largest organisation | Each group’s own records | 46 | 0.5202 | 0.6515 | 0.1313 |
| Without the largest organisation | Common: records in both groups | 46 | 0.5124 | 0.6692 | 0.1568 |
| Without the largest organisation | Common: equal per template | 46 | 0.5011 | 0.6593 | 0.1582 |
| Without the largest organisation, templates with ≥ 30 records in each group | Each group’s own records | 35 | 0.5202 | 0.6515 | 0.1313 |
| Without the largest organisation, templates with ≥ 30 records in each group | Common: records in both groups | 35 | 0.5124 | 0.6694 | 0.1569 |
| Without the largest organisation, templates with ≥ 30 records in each group | Common: equal per template | 35 | 0.4960 | 0.6593 | 0.1633 |

The band comparison was repeated within templates (Table S6). Throughout the band comparisons, each band excludes its lower bound and includes its upper bound. For templates with at least 30 member calculations in every governing-utilisation band, each band's deflection-governed share was averaged across templates with each template weighted by its total records, so the template mix is the same in every band. These templates held 1,408,076 of the 1,416,391 calculations. The deflection-governed share was higher in the highest band than in the lowest in 31 of the 40 templates, and in 30 of 39 without the largest organisation.

**Table S6. Deflection-governed share by governing-utilisation band, pooled and with template weights held fixed.**

| Governing utilisation | All calculations, pooled | All calculations, 40 templates standardised | Without the largest organisation, pooled | Without the largest organisation, 39 templates standardised |
| --- | ---: | ---: | ---: | ---: |
| ≤ 0.2 | 17.0% | 16.9% | 11.5% | 11.7% |
| 0.2–0.4 | 40.2% | 39.2% | 23.6% | 23.8% |
| 0.4–0.6 | 49.4% | 48.3% | 34.1% | 33.1% |
| 0.6–0.8 | 57.8% | 58.4% | 40.3% | 40.1% |
| > 0.8 | 63.7% | 67.0% | 45.0% | 47.2% |

A specification grid varied the lower inclusion threshold and whether de-duplication, applied after the threshold, was used (Table S7). The upper bound remained D/C ≤ 1. The bearing-inclusive columns describe a different population from the headline set and are shown for comparison. Records with utilisation above unity were summarised by check type.

**Table S7. Specification grid. Records entered when governing utilisation exceeded the lower threshold.**

| Lower threshold | De-duplicated | Strength n | Mean | Deflection n | Mean | Headline n | Mean | Incl. bearing n | Mean |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.00 | No | 735,572 | 0.4727 | 691,900 | 0.6258 | 1,427,472 | 0.5469 | 1,454,574 | 0.5499 |
| 0.00 | Yes | 729,207 | 0.4729 | 687,184 | 0.6259 | 1,416,391 | 0.5471 | 1,443,295 | 0.5501 |
| 0.05 | No | 713,943 | 0.4861 | 690,893 | 0.6267 | 1,404,836 | 0.5553 | 1,431,933 | 0.5581 |
| 0.05 | Yes | 707,881 | 0.4862 | 686,197 | 0.6268 | 1,394,078 | 0.5554 | 1,420,977 | 0.5582 |
| 0.10 | No | 660,378 | 0.5193 | 686,537 | 0.6302 | 1,346,915 | 0.5758 | 1,372,971 | 0.5788 |
| 0.10 | Yes | 654,905 | 0.5194 | 681,897 | 0.6303 | 1,336,802 | 0.5759 | 1,362,660 | 0.5789 |

Per-template results behind Tables S5 and S6 are not released (S2.3).

## S2.8 Prediction comparison settings

RQ4 compared three ridge regressions with one-hot categorical inputs: (a) template and creation month; (b) engineer-account-by-organisation and organisation identifiers, with month; and (c) the combined input set. The engineer-account-by-organisation identifier combines user_id and organisation_id, so a user occurring under two organisations has a separate category in each. Templates already encode material, member type and design-standard choices. The governing-check label was not used as an adjustment variable because it is determined by the stored maximum.

Three outer folds kept every project entirely in training or testing, and all models shared the same project folds within a population. Within each training fold, a fixed 20% project-grouped validation split selected the penalty from 0.1, 10 and 1,000; the outer test outcomes were not used for selection. Encoders were fitted only on training records and ignored unseen categories. Two records with a missing creation month were retained as a separate category. The split seed was 20261022; the LSQR solver used a tolerance of 10⁻⁷ and an iteration cap of 1,500.

Performance was summarised by pooled out-of-fold root mean squared error (RMSE), mean absolute error and R², using untruncated predictions. The paired reduction in squared prediction error when account inputs were added to template and month was accompanied by a 95% percentile interval from 1,000 organisation-cluster bootstrap draws of held-out error sums and record counts. This interval conditions on the fitted models; model fitting and tuning were not repeated within the bootstrap. The comparison was repeated without the largest organisation, with a reproducible cap of 2,000 records per organisation, and with the alternative de-duplication key that omits the governing reference. The capped sample describes a different record mixture from the full set. The evaluation concerns withheld projects within the observed platform population, largely for previously observed accounts, rather than entirely new engineers or firms.

The prediction comparison was run with Python 3.12.14, pandas 2.2.3, NumPy 2.3.5, SciPy 1.18.1 and scikit-learn 1.9.1.

## S2.9 Workflow

The workflow combined cleaning and analysis notebooks with versioned analysis and figure scripts. All analyses consumed typed, classified data products. The initial cleaning notebook used Python 3.11.8, pandas 3.0.3, NumPy 2.4.4, SciPy 1.17.1 and scikit-learn 1.9.0; these versions describe the initial cleaning stage rather than every subsequent analysis. The prediction comparison used the hashed-sheet-name product, fixed seeds, project-disjoint validation and recorded solver diagnostics; its source checksum, configuration, aggregate outputs and package versions are recorded with the script. Parser and classifier tests and a field dictionary support the pipeline. The uncertainty and robustness analyses in S2.7 were run on the same hashed-sheet-name product with Python 3.9.6, pandas 2.3.1 and NumPy 2.0.2; the headline set was reproduced exactly before they were run. Access to derived outputs and code is described in the paper's Data availability statement.
