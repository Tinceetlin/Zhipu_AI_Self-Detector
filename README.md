# Black-Box Provenance Self-Detection for Zhipu AI (GLM 5.2)

This repository contains the dataset, implementation scripts, and statistical evaluation code for the research paper titled: **"Black-Box Provenance Self-Detection on Zhipu AI GLM 5.2 Across Multiple Text Manipulations"**.

The primary objective of this study is to evaluate the capability of the GLM 5.2 model to detect its own generated or modified text via black-box API interactions, focusing on performance, calibration quality, stability, and statistical consistency.

---

## 📁 Repository Structure

```text
├── dataset/
│   ├── classification_result.xlsx    # 4,000 abstracts aggregated from 20,000 evaluations 
│   ├── evaluation_result.xlsx        # 20,000 evaluations obtained from 4,000 abstracts × 5 runs
|   ├── tbl_transformations.xlsx      # 1,000 control abstracts + 3,000 abstracts generated or modified by Z.AI
├── Prompt_engineering/
│   ├── AI-Generated_prompt.txt       # prompt script for generating a new abstract using the abstract title as a reference (AI-Generated) 
│   ├── AI-Paraphrase_prompt.txt      # prompt script for creating a new abstract by paraphrasing the original abstract (AI-Paraphrase)
│   └── AI-Rewrite_prompt.txt         # prompt script for creating a new abstract by rewriting the original while retaining the data and foreign terms (AI-Rewrite)
│   └── self-detection_prompt.txt     # prompt script for performing self-detection (classification)
├── statistical_test/
│   ├── Cochran Q                     # Cochran's-Q Test data and python source code
|   └── McNemar                       # Post-hoc McNemar data and python source code
|   └── Friedman                      # Friendman Test data and python source code
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

## 🤖 Black-Box Self-Detection Prompting

Since internal token log-probabilities are inaccessible via the Zhipu AI black-box API, we extract the proxy probabilities using a constrained **verbalized confidence score** prompt template:

```text
////////////////////////////////
/////Prompt Self-Detection /////
////////////////////////////////

You are acting as a Z.AI text detector.
Your task is to analyze the following research abstract and determine whether it was written by a non-Z.AI source or generated/modified using Z.AI.

Definitions:
non-Z.AI: An abstract written by a non-Z.AI source.
Z.AI: An abstract generated, paraphrased, or rewritten using a Z.AI model.

Base your analysis on linguistic characteristics, writing style, sentence structure, coherence, consistency, word choice, and other relevant textual patterns that may indicate whether the abstract was created by a non-Z.AI source or generated/modified by Z.AI.

Perform the test 5 times. For each test result, provide a response ONLY in the following JSON format:

{
"run": 1,
"prediction": "non-Z.AI or Z.AI",
"confidence_non-zai": <number between 0.0000 and 1.0000>,
"confidence_zai": <number between 0.0000 and 1.0000>,
"reason": "<maximum 300 words>"
}

Requirements:
* confidence_non-zai and confidence_zai must be decimal numbers with exactly four digits after the decimal point (e.g., 0.8734; 0.1356; 0.5078).
* confidence_non-zai + confidence_zai must equal 1.000 (with a rounding tolerance of ±0.001).
* confidence_non-zai represents your level of confidence that the abstract was written by a non-Z.AI source.
* confidence_zai represents your level of confidence that the abstract was generated or modified using Z.AI.
* prediction must correspond to the class with the higher confidence score.
* Do not include any explanations, comments, or additional text outside the JSON object.

Research Abstract:
<<< insert your abstract here >>>
```

---

## 📉 Evaluation Suite

The performance and reliability of the self-detection mechanism are rigorously verified using three primary dimensions:

### 1. Classification & Calibration Metrics
*   **Standard Performance:** Accuracy, Precision, Recall, F1-Score, and AUC-ROC.
*   **Calibration Quality:** **Brier Score** and **Expected Calibration Error (ECE)** to assess the alignment between verbalized confidence scores and empirical correctness, complemented by **Reliability Diagrams**.

### 2. Stability & Consistency Analysis
*   Standard Deviation ($SD$) and Prediction Entropy across iterative API calls.

### 3. Statistical Significance Testing
*   **Cochran’s Q Test:** Evaluates the binary detection accuracy significance across the 3 manipulation levels.
*   **Friedman Test:** Assesses variance differences in continuous verbalized confidence scores.
*   **Post-hoc McNemar Test (with Holm Correction):** Performs pairwise error-rate comparisons if the global null hypothesis ($H_0$) is rejected.

---

## 📝 Citation & Contact
This research is prepared for publication in **Jurnal ELTIKOM** (SINTA 2). For questions regarding replication or dataset usage, please open an Issue or contact the repository collaborators.

