# When does keeping the document during practice help?

When Does Document Replay Help Evidence-State Question Answering?

Wenzhang Du · Open Research Reports · v1.0.2 · 2026-11-22

Two adapters practised the same questions and answers, one with the documents and one without. On 32 paired inventory worlds, the document-trained adapter led by 19.25 percentage points with an unrelated synthetic record attached at test time. With a length-matched WikiText excerpt it trailed by 7.92 points. The order also reversed on 16 newly trained worlds.

[Original PDF](../paper/manuscript.pdf) · [Online report](https://dqswordman.github.io/technical-reports/document-replay-evidence-qa/)

## What the inventory reported and what the audit permits

Zubiru’s inventory lists Pihene as its storage bay. An audit rules out that assignment. Asked what the inventory said, the model should still answer Pihene. Asked what belongs in the verified catalogue, it should leave the value unspecified. A third question asks for the verification state itself. One fact earns credit only when all three answers agree with the evidence.

![An inventory example, evidence-status readouts, and practice with or without attached documents.](../figures/design.png)

Figure 1. Follow one disputed storage assignment through the three questions. The two training branches rehearse the same answers, with the supporting documents attached in only one branch.

## Keep the practice answers fixed and vary the test attachment

Both specialists start from the same mixed-practice checkpoint and take 40 additional updates on identical question–answer pairs. Branch A practises closed book. Branch B reads the documents during practice. At test time, both receive either an unrelated synthetic verification record or a WikiText passage matched in length. Joint accuracy counts facts for which all three answers are correct.

A third branch continues mixed practice. It matches the number of updates and supervised answers. Its later training mix and token count differ. The paired world is the uncertainty unit. The original specialist comparison uses 32 worlds; a fresh study trains new adapters on 16 new worlds.

## Changing the test attachment reverses which specialist leads

With synthetic attachments, document replay beats closed-book replay by 19.25 percentage points on the original 32 worlds. With WikiText it trails by 7.92 points (paired 95% interval for document minus closed-book replay, −12.53 to −3.55). On 16 fresh worlds both directions recur. On the original worlds a third adapter that continued mixed practice leads even the stronger specialist on each attachment type.

Differences in joint accuracy, in percentage points, paired within world. B−A subtracts closed-book from document replay. The last row compares continued mixed practice with the better specialist separately for each attachment.

| Comparison | Worlds | Synthetic | WikiText |
| --- | --- | --- | --- |
| B − A | 32 | +19.25 | −7.92 |
| B − A | 16 | +17.16 | −6.89 |
| MIX120 − stronger specialist | 32 | +5.58 | +9.23 |

[Source table](https://github.com/dqswordman/document-replay-evidence-qa/blob/v1.0.1/reference/paper_comparisons.csv)

## How much can presentation alone explain?

Keep the donor facts fixed and rewrite the synthetic record as prose. With explicit verdict cues, that change reduces the document-trained branch’s lead by 3.20 points. All four combinations of presentation and review cue still favor that branch. Reformatting these facts explains part of the change in its lead, while the reversal under WikiText remains unexplained.

The experiments use one Qwen3-1.7B backbone, synthetic worlds and multiple-choice outputs. Length matching leaves differences in vocabulary, discourse and familiarity. Real catalogues also require open-ended answers, source credibility and a cost model for incorrect entries. Those decisions lie beyond these readouts.

## Rebuild joint accuracy from individual choices

The release includes individual choices, world-level scores, fixed question plans and source attribution. On CPU, the replay checks 435,456 choices from the three follow-up studies, verifies 472 paired effects and writes 17 comparisons. The result map identifies the archived evidence for the earlier synthetic analyses and the original WikiText comparison.

The released context schedule verifies 1,440 mixed slots per world across 32 worlds. Recombining the document and question losses also recovers all 7,680 logged training-step objectives in the mixed and new-world studies. The adapter and Adam routines are included.

```sh
python -B verify_manifest.py
python -B reproduce.py --out replay
python -B check_methods.py
```

## Citation and materials

[Original manuscript · PDF](https://dqswordman.github.io/assets/reports/document-replay-evidence-qa/manuscript.pdf) · [Frozen release and checksums](https://github.com/dqswordman/document-replay-evidence-qa/releases/tag/v1.0.1) · [Result map and reproduction scope](https://github.com/dqswordman/document-replay-evidence-qa/blob/v1.0.1/docs/reproduction.md) · [Interactive evidence explorer](https://huggingface.co/spaces/DQSWORDMAN/document-replay-evidence-qa) · [Method implementation and worked checks](https://github.com/dqswordman/document-replay-evidence-qa/blob/v1.0.1/docs/methods.md)
