# LLMs Metrics

Evaluation framework for measuring LLM performance on Colombian idioms (modismos) using multiple metrics.

## Overview

This project evaluates Large Language Models on their ability to define Colombian idiomatic expressions across three prompts using automated metrics (BERTScore, Sentence-BERT, chrF) and human evaluation.

## Structure

```
LLMs_Metrics/
├── CodeMetrics/          # Metric implementations
│   ├── BertScore.py      # BERTScore with BETO and SciBETO
│   ├── SentenceBert.py   # Sentence-BERT semantic similarity
│   └── chrF.py           # Character n-gram F-score
├── DataSet/              # Evaluation datasets
├── LLMs_Results/         # Model output data (3 prompts)
├── Metrics_Results/      # Computed metric scores
├── Human_Metrics/        # Human evaluation data
├── Ranking_Results/      # Model rankings
├── ComputeMetrics.ipynb  # Main metrics computation
├── Geo_Analysis.ipynb    # Geographic analysis
└── RankingModels.ipynb   # Model ranking analysis
```

## Metrics

- **BERTScore**: Contextual embeddings (BETO, SciBETO)
- **Sentence-BERT**: Semantic similarity (multilingual-mpnet, xlm-roberta, scibeto)
- **chrF**: Character-level n-gram matching
- **Accuracy**: Exact match for prompt 1

## Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Place LLM results in `LLMs_Results/`
3. Run `ComputeMetrics.ipynb` to compute metrics
4. Use `RankingModels.ipynb` for model comparison
5. Analyze geographic patterns with `Geo_Analysis.ipynb`

## Data

- **DataSet_ConEjemplos.json**: Dataset with usage examples
- **DataSet_PrimeraOcurrencia.json**: First occurrence dataset
- **DataSet_ConRegión.json**: Regional information
- **prompt_X_metrics_data.json**: LLM responses per prompt

## Requirements

Python 3.8+, PyTorch, Transformers, Sentence-Transformers, BERT-Score, pandas, numpy, matplotlib, seaborn
