# CodeAlpha Task 4 — Sentiment Analysis

This project covers Task 4: Sentiment Analysis from the CodeAlpha Data Analytics task list.

## Features
- Reads review text from a CSV file.
- Uses VADER sentiment scoring to classify text as Positive, Negative, or Neutral.
- Exports row-level scores and predicted labels to CSV.
- Prints a summary of predicted sentiment counts.

## Setup (Windows PowerShell)
Open this folder in VS Code and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run Task 4
```powershell
python src/sentiment_analysis.py
```

Default input: `data/sample_reviews.csv`
Output: `outputs/sentiment_results.csv`

## Use your own reviews
```powershell
python src/sentiment_analysis.py --input data/my_reviews.csv --text-column Review
```
Change `Review` to the name of your text column.

## Method
VADER compound score ranges from -1 to +1:
- >= 0.05: Positive
- <= -0.05: Negative
- otherwise: Neutral

## Limitations
This is a lexicon-based educational baseline. It can misread sarcasm, context, slang, mixed-language text, and domain-specific expressions. The sample reviews are illustrative and not representative of real customer opinions. Validate against labeled data before making real-world claims.
