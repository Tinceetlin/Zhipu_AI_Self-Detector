# Black-Box Provenance Self-Detection for Zhipu AI (GLM 5.2)

This repository contains the dataset, implementation scripts, and statistical evaluation code for the research paper titled: **"Black-Box Provenance Self-Detection on Zhipu AI GLM 5.2 Across Multiple Text Manipulations"**.

The primary objective of this study is to evaluate the capability of the GLM 5.2 model to detect its own generated or modified text via black-box API interactions, focusing on performance, calibration quality, stability, and statistical consistency.

---

## 📁 Repository Structure

``text
├── DATASET/
│   ├── MASTER RUNS.xlsx          # 20.000 evaluations from 5 runs * (1.000 abstracts human-written + 1.000 AI-Generated + 1.000 AI-Rewrite + 1.000 AI-Paraphrase)
│   ├── HASIL KLASIFIKASI.xlsx    # 1.000 abstracts human-written + 1.000 AI-Generated + 1.000 AI-Rewrite + 1.000 AI-Paraphrase
├── Prompt_engineering/
│   ├── AI-Generated_prompt.txt       # prompt script for generating a new abstract using the abstract title as a reference (AI-Generated) 
│   ├── AI-Paraphrase_prompt.txt      # prompt script for creating a new abstract by paraphrasing the original abstract (AI-Paraphrase)
│   └── AI-Rewrite_prompt.txt         # prompt script for creating a new abstract by rewriting the original while retaining the data and foreign terms (AI-Rewrite)
│   └── self-detection_prompt.txt     # prompt script for performing self-detection (classification)
├── results/
│   ├── Cochran's-Q Test        # Cochran's-Q Test result
│   └── Post-hoc McNemar        # Post-hoc McNemar
└── README.md                   # Project documentation
```

---

## 📊 Experimental Setup & Datasets

This study employs a **within-subject / repeated measures design** leveraging a total of **4,000 unique text samples** divided across three evaluation scenarios:

*   **Baseline (Control Group):** 1,000 human-written research abstracts. This identical set is kept constant across all experiments to control for textual background variability.
*   **Dataset #1 (AI-Paraphrase):** 1,000 human abstracts processed through AI paraphrasing.
*   **Dataset #2 (AI-Rewrite):** 1,000 human abstracts processed through AI rewriting.
*   **Dataset #3 (AI-Generated):** 1,000 purely AI-generated abstracts based on corresponding keywords.

---

## 🤖 Black-Box Confidence Prompting

Since internal token log-probabilities are inaccessible via the Zhipu AI black-box API, we extract the proxy probabilities using a constrained **verbalized confidence score** prompt template:

```text
[System Prompt]
You are a highly objective text analysis system. Analyze the following text and determine if it was authored by a human or generated/manipulated by an AI model.

You MUST respond strictly in the following format and provide exact decimal values:
confidence AI= [Value between 0-1]
confidence Human= [Value between 0-1]

Constraint: The sum of confidence AI and confidence Human must exactly equal 1.0. Do not include any other text, explanation, or markdown formatting.
```

---

## 📉 Evaluation Suite

The performance and reliability of the self-detection mechanism are rigorously verified using three primary dimensions:

### 1. Classification & Calibration Metrics
*   **Standard Performance:** Accuracy, Precision, Recall, F1-Score, and AUC-ROC.
*   **Calibration Quality:** **Brier Score** and **Expected Calibration Error (ECE)** to assess the alignment between verbalized confidence scores and empirical correctness, complemented by **Reliability Diagrams**.

### 2. Stability & Consistency Analysis
*   Standard Deviation ($SD$), Prediction Entropy, and Prediction Consistency across iterative API calls.

### 3. Statistical Significance Testing
*   **Cochran’s Q Test:** Evaluates the binary detection accuracy significance across the 3 manipulation levels.
*   **Friedman Test:** Assesses variance differences in continuous verbalized confidence scores.
*   **Post-hoc McNemar Test (with Holm Correction):** Performs pairwise error-rate comparisons if the global null hypothesis ($H_0$) is rejected.

---

## 📝 Citation & Contact
This research is prepared for publication in **Jurnal ELTIKOM** (SINTA 2). For questions regarding replication or dataset usage, please open an Issue or contact the repository collaborators.

