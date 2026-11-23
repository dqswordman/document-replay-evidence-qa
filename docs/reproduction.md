# Reproducing the reported results

**When Does Document Replay Help Evidence-State Question Answering?** · Wenzhang Du · v1.0.1

The replay starts from saved choices or world-level summaries, according to the study. It reconstructs joint accuracy for each attachment condition and compares the training branches within world. The commands below reproduce the released comparisons on CPU.

```sh
python -m pip install -r requirements.txt
python -B verify_manifest.py
python -B reproduce.py --out replay
```

Run the commands at the root of the extracted archive with Python 3.12. CPU verification uses NumPy 2.5.3, the version used to check this release. The manifest verifies the publication files before replay. A successful run prints `PASS` and writes its derived tables or summary into the empty output directory.

| Study result | Files | Unit and operation |
| --- | --- | --- |
| Original synthetic and WikiText specialists | [Input](../results/original_natural_effects.csv) · [Reference](../results/original_wikitext/per_parent_metrics.csv) | 32 worlds. The original synthetic effects are archived summaries. The original WikiText bundle adds world- and article-level scores. |
| Same-fact, mixed and fresh-world studies | [Input](../results/bridge_query_scores.csv.xz) · [Reference](../reference/paper_comparisons.csv) | 435,456 question readouts across three follow-ups. Join source, status and return-value decisions within the record and average rotations within each world. |
| Paired uncertainty and study coverage | [Input](../results/paired_effects.csv) · [Reference](../reference/comparison_checks.json) | Rebuild and compare 472 paired rows, then export the 17 paper comparisons with their signed direction and number of worlds. |

## Evidence boundaries

The package includes frozen construction and scoring plans, readout choices, parent-level summaries, training traces where available, and original model and adapter identities. It supports CPU recovery from archived choices. A new adapter-training run requires the upstream model and a training environment. The original synthetic study is supplied at summary level and the original WikiText study at world/article level.

The tasks use synthetic inventories and one 1.7B model. Continued mixed practice matches the specialists on updates and supervised answers. Training token counts differ. For a single worked case, run `python -B example.py`. [Original manuscript](../paper/manuscript.pdf) · [English report](report.en.md) · [中文报告](report.zh.md) · [Third-party terms](../THIRD_PARTY_NOTICES.md)

## Method implementation

The [mixed-context scheduler](../code/mixed_schedule.py) and [adapter and optimizer](../code/adapter_optimizer.py) expose the original branch-balancing rules and parameter updates. The CPU check reads every released mixed schedule and verifies step identities, prompt-context counts and all saved mixed and fresh-world step losses. The optional optimizer module uses PyTorch. The scientific CPU checks use NumPy and the standard library.

Run `python -B check_methods.py`. [Method guide](methods.md)
