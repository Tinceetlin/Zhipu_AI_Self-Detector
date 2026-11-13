Companion code and data for the paper *Black-Box Detection of Z.AI-Generated and Modified Academic Abstracts Against Human-Written Controls: Discrimination, Calibration, and Repeatability of GLM-5.2 Verbalized Confidence* (Sir & Tallo). Concept DOI: **[FILL IN: Zenodo concept DOI after the first release is synced]**.

## Highlights (key findings)

GLM-5.2 (Z.AI), queried as a black box with a fixed prompt, had to separate 1,000 human-written abstracts from 1,000 Z.AI variants per condition. The Z.AI-class score is the mean of five within-response judgments; the decision threshold is 0.5. 95% CIs are percentile intervals from 10,000 source-family bootstrap replicates.

| Condition (vs. same 1,000 controls) | Accuracy (95% CI) | F1 (AI class) | ROC-AUC (95% CI) | Brier Score (95% CI) | ECE, 10 bins (95% CI) | False-negative rate |
|---|---|---|---|---|---|---|
| Generate | 97.55% (96.85–98.20) | 97.58% | 0.9952 (0.9926–0.9973) | 0.0354 (0.0319–0.0390) | 0.1019 (0.0955–0.1087) | 1.30% |
| Rewrite | 89.10% (87.80–90.35) | 88.24% | 0.9472 (0.9372–0.9566) | 0.0920 (0.0850–0.0993) | 0.0781 (0.0685–0.0904) | 18.20% |
| Paraphrase | 85.60% (84.20–87.00) | 83.86% | 0.9266 (0.9155–0.9372) | 0.1147 (0.1066–0.1230) | 0.0828 (0.0742–0.0948) | 25.20% |

False-positive rate on the human controls: 3.60% (36/1,000), identical in all three scenarios because the same controls are reused.

**What the numbers say**

- **Detection depends on the manipulation.** Accuracy differs across the three scenarios (Cochran's Q = 248.17, df = 2, p < 0.005). All pairwise McNemar tests with Holm correction are significant: Generate vs. Rewrite χ² = 154.229508 (p_Holm = 4.126696 × 10⁻³⁵); Generate vs. Paraphrase χ² = 218.702703 (p_Holm = 5.205737 × 10⁻⁴⁹); Rewrite vs. Paraphrase χ² = 16.531250 (p_Holm = 4.785484 × 10⁻⁵).
- **Best discrimination is not best calibration.** Generate has the highest ROC-AUC and lowest Brier Score but the highest ECE. Paired ΔECE (Holm-adjusted): Generate − Rewrite = 0.0237 (95% CI 0.0107–0.0345, p < 0.001); Generate − Paraphrase = 0.0190 (0.0059–0.0292, p = 0.003); Rewrite − Paraphrase = −0.0047 (−0.0184 to 0.0083, p = 0.548, not significant). The Rewrite/Paraphrase ECE ordering flips across 5/10/15/20 bins, while Generate has the highest ECE under all four.
- **Repeatability differs by condition.** Five-way label agreement (5:0): Generate 98.20%, Rewrite 92.60%, Paraphrase 90.10%, human controls 95.90%. Median between-judgment score SD: 1.71, 2.58, 2.70 and 2.14 percentage points, respectively. Friedman tests across the three scenarios: confidence χ² = 571.095 and score SD χ² = 340.337 (df = 2, both p < 0.001).
- **Agreement is not correctness.** 88.10% of missed Paraphrase texts (222/252) and 66.67% of false-positive controls (24/36) received the same wrong label in all five judgments.

## Types of text manipulation

Three manipulations, each applied by GLM-5.2 itself to every source abstract (K = 3). Prompts are in `Prompt_engineering/`.

| Condition | What was done | Input to Z.AI |
|---|---|---|
| **Generate** | A new abstract written from the paper title only (maximum 300 words). | Title |
| **Rewrite** | Complete rewrite in a new linguistic style while keeping all numbers, metrics and facts; clichéd AI phrasing to be avoided. | Source abstract |
| **Paraphrase** | Copy-editing style paraphrase that changes wording and sentence structure while keeping technical content. | Source abstract |

Not tested: summarization, translation, character- or token-level perturbation, third-party "humanizer" tools, cascaded/repeated manipulations, or text from any LLM other than GLM-5.2.

## Dataset

| Item | Value |
|---|---|
| Source corpus | *arXiv Paper Abstracts* (Paul & Rakshit, Kaggle) |
| Eligibility | English, Computer Science, archived on or before September 30, 2021 (54,230 eligible abstracts) |
| Selection | First 1,000 complete source families in dataset order; no random sampling, so no sampling seed. 152 sources were excluded for failed transformation or classification validation and replaced by the next record |
| N (source abstracts) | 1,000 |
| K (manipulation types) | 3 (Generate, Rewrite, Paraphrase) |
| Texts | 4,000 = 1,000 human controls + 3 × 1,000 Z.AI variants |
| R (repeats) | 5 judgments per text, produced within one API response (not five separate calls) |
| Judgment-level outputs | 20,000 (4,000 requests × 5) |
| Labels | Binary: `non-Z.AI` (human control, 0) and `Z.AI` (generated/modified, 1; positive class). Each judgment is JSON with `run`, `prediction`, `confidence_non-zai`, `confidence_zai` (four decimals, summing to 1.000 ± 0.001) and `reason`. `text_id` groups the five judgments of a text; `source_id` links a control to its three variants |

Files in `dataset/`: `tbl_transformations.xlsx` (1,000 controls + 3,000 variants), `evaluation_result.xlsx` (20,000 judgments), `classification_result.xlsx` (4,000 texts aggregated from the 20,000 judgments).

## Reproducibility

| Item | Value |
|---|---|
| Model / endpoint | `glm-5.2` via `https://api.z.ai/api/paas/v4/chat/completions` |
| API snapshot date | All transformation and classification calls were made between **July 22 and August 16, 2026**. No immutable model snapshot or build identifier was recorded |
| Parameters | temperature 0.0; thinking type enabled; reasoning_effort max |
| Context isolation | Each abstract in a fresh request: current prompt plus abstract only, no history |
| Aggregation | Per-text mean of the five `confidence_zai` values; decision threshold 0.5 (≥ 0.5 → Z.AI) |
| Statistics | 10,000 source-family bootstrap replicates (95% percentile CIs); 10,000 paired randomization replicates for ECE differences; Holm correction; Cochran's Q, McNemar (Yates), Friedman |
| Python version | **[FILL IN: output of `python --version`]** |
| Zhipu/Z.AI SDK or HTTP client + version | **[FILL IN: e.g., output of `pip show <package>`; the paper reports only the REST endpoint]** |
| Random seeds | None for source selection (sequential). Bootstrap/randomization seed: **[FILL IN from code, or state "not set"]** |
| Number of API requests | At least 7,000 successful (3,000 transformations + 4,000 classifications), plus requests for the 152 excluded sources (count not reported) |
| Cost and wall-clock time | **[FILL IN from Z.AI billing/usage log and run logs]** |

Because GLM-5.2 is a hosted commercial model, re-running the API calls may not reproduce the released outputs exactly. The released spreadsheets are the reference data for the paper's numbers.

## Quickstart

```bash
git clone https://github.com/Tinceetlin/Zhipu_AI_Self-Detector.git
cd Zhipu_AI_Self-Detector
python -m venv .venv && source .venv/bin/activate
pip install pandas openpyxl
python - <<'EOF'
import pandas as pd
for f, n in [("dataset/tbl_transformations.xlsx", 4000), ("dataset/evaluation_result.xlsx", 20000), ("dataset/classification_result.xlsx", 4000)]:
    df = pd.read_excel(f); print(f, df.shape, "OK" if len(df) == n else "MISMATCH", list(df.columns))
EOF
```

This checks the file sizes stated above (4,000 / 20,000 / 4,000 rows) and prints the column names. **[FILL IN: add one command that recomputes the Table 4 metrics once the metric script is in the repository.]**

## Known limitations

- **One model only.** Only GLM-5.2 (Z.AI) was evaluated; results do not transfer to other models.
- **Black-box protocol.** Only labels and verbalized confidence were used; no logits, weights or hidden activations. The results are not evidence of an internal self-recognition mechanism.
- **Snapshot may change.** The hosted API can change; no immutable snapshot ID was recorded (collection window July 22 to August 16, 2026).
- **Human-only negatives.** The negative class has no outputs from other LLMs, so the study cannot separate Z.AI-specific recognition from sensitivity to generic LLM cues.
- **Scope.** English Computer Science abstracts, one prompt and one API configuration. Prompt wording and API settings were not varied.
- **Limited repeatability window.** Five judgments come from a single response; they do not show long-term stability.
- **Selection and reuse.** 152 sources were excluded for processing failures (possible selection effect, not quantified). The same 1,000 controls appear in all three scenarios, and the 2021 cutoff does not rule out overlap with the model's training data.
- **No same-data baseline.** No other detector or LLM judge was run on these 4,000 texts.

## Ethics statement

- **Not proof of authorship.** Scores are decision-support evidence for preliminary screening only. Do not use them as the sole basis for an academic-integrity decision. On human-written abstracts the false-positive rate was 3.60%, and the Paraphrase condition missed 25.20% of Z.AI-modified texts.
- **What is released.** Study data, prompts and statistical outputs for replication. No trained classifier, model weights or ready-to-use detection application. `self-detection_prompt.txt` is the verbatim prompt used in the experiment.
- **Dual-use materials.** The Rewrite and Paraphrase prompts were written to alter wording and style (for example, to avoid stock AI phrasing and to lower similarity scores). They are released to document the experiment and must not be used to disguise AI involvement where disclosure is required.
- **Data.** Human abstracts come from a public arXiv-derived dataset; no private or personal data were collected.
- **AI assistance.** The authors report using ChatGPT for literature-candidate identification, reference checking, language editing and paraphrasing of manuscript text, and take responsibility for the content.

## Licenses

| Component | License |
|---|---|
| Code and scripts | MIT (`LICENSE`) |
| Dataset (`dataset/`) | **[DECIDE: CC-BY-4.0 or CC-BY-NC-4.0 (`LICENSE-DATA`); confirm the terms of the Kaggle source dataset and Z.AI output terms first]** |

## How to cite

Cite the paper once it is published; until then cite the archived release.

```bibtex
@article{sir2026blackbox,
  title     = {Black-Box Detection of {Z.AI}-Generated and Modified Academic Abstracts Against Human-Written Controls: Discrimination, Calibration, and Repeatability of {GLM-5.2} Verbalized Confidence},
  author    = {Sir, Yosua Alberth and Tallo, Tince Etlin},
  journal   = {Jurnal ELTIKOM: Jurnal Teknik Elektro, Teknologi Informasi dan Komputer},
  volume    = {FILL IN},
  number    = {FILL IN},
  pages     = {FILL IN},
  year      = {2026},
  publisher = {P3M Politeknik Negeri Banjarmasin},
  issn      = {2598-3288},
  doi       = {FILL IN}
}

@software{sir2026zhipu_self_detector,
  title     = {Zhipu\_AI\_Self-Detector: Replication package for black-box detection of {Z.AI}-generated and modified academic abstracts},
  author    = {Sir, Yosua Alberth and Tallo, Tince Etlin},
  year      = {2026},
  version   = {v1.0.0},
  publisher = {Zenodo},
  doi       = {FILL IN},
  url       = {https://github.com/Tinceetlin/Zhipu_AI_Self-Detector}
}
```
