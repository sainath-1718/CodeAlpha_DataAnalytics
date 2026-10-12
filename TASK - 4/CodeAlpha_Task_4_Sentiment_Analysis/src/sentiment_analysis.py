import argparse
from pathlib import Path
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "sample_reviews.csv"
OUTPUT = ROOT / "outputs" / "sentiment_results.csv"

def classify(compound: float) -> str:
    if compound >= 0.05:
        return "Positive"
    if compound <= -0.05:
        return "Negative"
    return "Neutral"

def main():
    parser = argparse.ArgumentParser(description="Classify review text as positive, negative, or neutral.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Path to a CSV file with review text.")
    parser.add_argument("--text-column", default="Review", help="Column containing review text.")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input CSV not found: {input_path}")
    df = pd.read_csv(input_path)
    if args.text_column not in df.columns:
        raise SystemExit(
            f"Text column '{args.text_column}' not found. Available columns: {', '.join(map(str, df.columns))}"
        )
    if df.empty:
        raise SystemExit("Input CSV has no rows.")

    analyzer = SentimentIntensityAnalyzer()
    result = df.copy()
    text = result[args.text_column].fillna("").astype(str)
    scores = text.apply(lambda value: analyzer.polarity_scores(value))
    result["Sentiment_Negative_Score"] = scores.apply(lambda score: score["neg"])
    result["Sentiment_Neutral_Score"] = scores.apply(lambda score: score["neu"])
    result["Sentiment_Positive_Score"] = scores.apply(lambda score: score["pos"])
    result["Sentiment_Compound_Score"] = scores.apply(lambda score: score["compound"])
    result["Predicted_Sentiment"] = result["Sentiment_Compound_Score"].apply(classify)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

    print("CODEALPHA TASK 4 — SENTIMENT ANALYSIS")
    print("====================================")
    print(f"Input file: {input_path}")
    print(f"Rows analyzed: {len(result)}")
    print("\\nPredicted sentiment counts:")
    print(result["Predicted_Sentiment"].value_counts().to_string())
    print(f"\\nDetailed results saved to: {OUTPUT}")
    print("\\nNote: predictions are lexicon-based and should be manually reviewed.")

if __name__ == "__main__":
    main()
