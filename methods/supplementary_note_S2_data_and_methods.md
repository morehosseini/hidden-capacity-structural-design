# Supplementary Note S2. Data and methods details

Version 1.1.0 · 27 October 2026

This note accompanies Section 3 of Paper A, *Hidden Capacity in Everyday Structural Design*. It records the field definitions, platform behaviour confirmed by the operator, classification and storage rules, de-duplication tests and model settings that the main text summarises. All counts refer to the Calcs.com export analysed in the paper. The underlying calculation records are held by Calcs.com and are not part of this repository; access is described in the paper's Data availability statement.

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

The headline population contained 3,073 distinct user identifiers and 1,735 organisation identifiers. Each user identifier was treated as an engineer account; an account is not independently verified as a distinct professional engineer. Every project belonged to one organisation at the time of export, while 21 of the 3,073 user identifiers occurred under more than one organisation in the headline population. The operator attributed such cases mainly to support access, changes of membership or moved projects. Some projects involved more than one engineer, so projects and engineer accounts did not form a strictly nested hierarchy.

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

Shared names were rare. Of the 1,427,472 valid strength and deflection records, 98.1% had a combination of project, template and sheet name that no other record shared. Where a name was shared, the records resembled iterations of one member: 96.5% of the shared-name groups came from a single engineer, and in 63.0% all records were created within one hour. Because the key includes the governing reference, a member whose governing check changed between iterations can appear more than once, as happened in 40.2% of the shared-name groups. Removing the reference from the key reduced the set by 4,712 records (0.3%) and changed the mean by less than 0.001. A recalculation saved under a different sheet name can be retained more than once.

Sheet names can contain personal information. They were held internally under the operator's conditions, used only inside the de-duplication key, and never analysed, reported or released.

## S2.7 Uncertainty and robustness

Uncertainty for the headline mean used an engineer-clustered bootstrap with 1,000 replicates and seed 20260910. Four robustness procedures were applied. Aggregation sensitivity recomputed the governing mean with each record, project, engineer, material group or limit-state group weighted equally. A largest-account sensitivity repeated the main analyses with and without the single account that supplied about half of the records. A specification grid varied the lower inclusion threshold (0, 0.05 and 0.10) and whether de-duplication was applied. A template-coverage decomposition compared templates observed in both governing groups with those observed in only one. Records with utilisation above unity were summarised by check type.

## S2.8 Prediction comparison settings

RQ4 compared three ridge regressions with one-hot categorical inputs: (a) template and creation month; (b) engineer-account × organisation and organisation identifiers, with month; and (c) the combined input set. Templates already encode material, member type and design-standard choices. The governing-check label was not used as an adjustment variable because it is determined by the stored maximum.

Three outer folds kept every project entirely in training or testing, and all models shared the same project folds within a population. Within each training fold, a fixed 20% project-grouped validation split selected the penalty from 0.1, 10 and 1,000; the outer test outcomes were not used for selection. Encoders were fitted only on training records and ignored unseen categories. Two records with a missing creation month were retained as a separate category. The split seed was 20261022; the LSQR solver used a tolerance of 10⁻⁷ and an iteration cap of 1,500.

Performance was summarised by pooled out-of-fold root mean squared error (RMSE), mean absolute error and R², using untruncated predictions. The paired reduction in squared prediction error when account inputs were added to template and month was accompanied by a 95% percentile interval from 1,000 organisation-cluster bootstrap draws of held-out error sums and record counts. This interval conditions on the fitted models; model fitting and tuning were not repeated within the bootstrap. The comparison was repeated without the largest organisation, with a reproducible cap of 2,000 records per organisation, and with the alternative de-duplication key that omits the governing reference. The capped sample describes a different record mixture from the full set. The evaluation concerns withheld projects within the observed platform population, largely for previously observed accounts, rather than entirely new engineers or firms.

The prediction comparison was run with Python 3.12.14, pandas 2.2.3, NumPy 2.3.5, SciPy 1.18.1 and scikit-learn 1.9.1.

## S2.9 Workflow

The workflow combined cleaning and analysis notebooks with versioned analysis and figure scripts. All analyses consumed typed, classified data products. The prediction comparison used the hashed-sheet-name product, fixed seeds, project-disjoint validation and recorded solver diagnostics; its source checksum, configuration, aggregate outputs and package versions are recorded with the script. Parser and classifier tests and a field dictionary support the pipeline. Access to derived outputs and code is described in the paper's Data availability statement.
