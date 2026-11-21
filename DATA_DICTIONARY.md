# Data dictionary

All scientific tables are UTF-8 CSV. JSONL stores one object per line. A percentage reports accuracy, while `*_pp` denotes a difference in percentage points. Absolute-level rows in `paired_effects.csv` also use the 0–100 scale. The column `rate` in a world-level table is a proportion between zero and one.

| Field or file family | Meaning |
|---|---|
| `dataset`, `role`, `parent` | Same-fact (bridge), mixed continuation (mixed), or new worlds (transfer). Role P is technical calibration, T the main evaluation. A parent world is the independent unit. |
| `arm`, `condition` | A is closed-book replay, B document replay, M80 the shared mixed checkpoint, and M120 continued mixed practice. Conditions distinguish question alone, synthetic verification records, WikiText and the four same-fact renderings. |
| `C`, `T`, `W`, `J` | Source report, verification state, returnable value, and the conjunction of the three decisions for the same record. The five W rotations are averaged within the unit. |
| `target_status` | E is established, R ruled out, U unresolved, nonE combines R and U. W returns the reported value on E and the explicit None option on R or U. |
| `cell_id`, `slot`, `query_pair_id`, `atom_id`, `rotation_id` | Condition execution cell, question position, pairing key, record, and W option rotation. Version and template stay within their world. |
| `gold_index`, `pred_index`, `correct`, `status` | Candidate indices are zero based. An incorrect answer remains a valid measurement with correct=0. Empty prediction fields denote an unavailable or inapplicable value. |
| `p_A`…`p_E`, `lp_A`…`lp_E`, `mass` | Probabilities normalized over available letters, their full-vocabulary log probabilities, and total available-letter mass. Shorter candidate lists leave remaining letters empty. |
| `J_valid`, `J_correct` | Stored on return-value rows. Link them to the record's source and status answers to reconstruct the joint decision. |
| `*_parent_metrics.csv` | One world × arm × input × metric × target-state group. Planned, valid and numerator give the planned trials, measured trials and correct answers. WikiText each-article rows also have a pooled wiki row. |
| `*_coverage.csv` | Planned, actual, missing and invalid measurements for each evaluation cell. |
| `*_training_steps.csv.xz` | One saved optimization step with its measured objective and accounting fields. |
| `paired_effects.csv` | Cohort, named comparison, metric and state form a unique key. The sample size is in worlds. Estimate, percentile limits and sample standard deviation use the indicated units. |
| `reference/paper_comparisons.csv` | Specifies the direction of every displayed difference. MIX120 gains take the stronger measured specialist as reference for each input. |
| `config/<dataset>/` | Frozen construction, model and material seeds, input layouts, template families, cell plans, material digests and weight identities. |

For the original 32-world results, `prose` means WikiText. In the same-fact experiment, prose means a continuous rendering of the synthetic donor's own facts. A neutral review describes the catalogue entry in place of an explicit verdict. The two uses of prose refer to different input populations. The two cohorts are reported separately.

The original prospective readout and the new-world study assign two articles per main world. Each article, target version, question template and return-option rotation stays inside the world for confidence intervals. The three query score tables use XZ-compressed CSV files. They include the original full columns for question pairing, frozen weights, seeds, token positions and cell costs. Timing fields repeat across a cell's questions. Sum them once per cell.
