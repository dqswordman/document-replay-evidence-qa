# Third-party sources

## WikiText excerpts

Wikipedia contributors authored the article text. Stephen Merity and colleagues at Salesforce compiled WikiText. These experiments use the training split of WikiText-2 Raw v1 at revision `b08601e04326c79dfdd32d625aee71d232d685c3`. The upstream dataset lists CC BY-SA 3.0 and the GNU Free Documentation License. These terms continue to apply to the embedded Wikipedia/WikiText text, including copies inside prompts and training or evaluation material. [Pinned dataset card](https://huggingface.co/datasets/Salesforce/wikitext/tree/b08601e04326c79dfdd32d625aee71d232d685c3) · [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) · [GNU Free Documentation License](https://www.gnu.org/licenses/fdl.html)

The material-selection procedure removes title lines when constructing article bodies, normalizes line endings and selects contiguous excerpts at word boundaries. It preserves the upstream wording and corpus tokenization. The article inventory identifies 68 original selections (64 main and four calibration) and 32 new-world selections, their titles, world assignments, corpus row identifiers and content hashes. [Article inventory](attribution/wikitext_articles.csv) · [Original excerpt ranges](attribution/original_excerpt_ranges.csv) · [Source revision and shard digest](attribution/dataset.json) · [Data paper](https://openreview.net/forum?id=Byj72udxe)

## Model and dependencies

The original experiments use Qwen/Qwen3-1.7B at revision `70d244cc86ccca08cf5af4e1e306ecf908b1ad5e`. The checkpoint is supplied separately by its publisher under the terms of the model repository. This release contains the recorded model identity and weight digests. Python dependencies retain their own licenses. The CPU statistics require NumPy. [Qwen model and license](https://huggingface.co/Qwen/Qwen3-1.7B/tree/70d244cc86ccca08cf5af4e1e306ecf908b1ad5e) · [Dependency versions](environment.json)

Figure 1 depicts the experimental design. The remaining figures appear in the archived manuscript.
