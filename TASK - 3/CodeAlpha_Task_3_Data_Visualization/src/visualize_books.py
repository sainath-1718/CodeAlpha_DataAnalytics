from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "books_dataset.csv"
CHARTS = ROOT / "outputs" / "charts"

def save_chart(filename):
    plt.tight_layout()
    plt.savefig(CHARTS / filename, dpi=180, bbox_inches="tight")
    plt.close()

def main():
    if not DATA.exists():
        raise SystemExit(
            f"Dataset not found: {DATA}\n"
            "Copy your Task 1 books_dataset.csv into the data folder and run again."
        )

    df = pd.read_csv(DATA)
    if df.empty:
        raise SystemExit("The dataset is empty. Add book records and try again.")

    CHARTS.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")
    generated = []

    if "Price_GBP" in df.columns:
        df["Price_GBP"] = pd.to_numeric(df["Price_GBP"], errors="coerce")
        prices = df["Price_GBP"].dropna()
        if not prices.empty:
            plt.figure(figsize=(9, 5.5))
            sns.histplot(prices, bins="auto", kde=len(prices) >= 5)
            plt.title("Distribution of Book Prices")
            plt.xlabel("Price (£)")
            plt.ylabel("Number of Books")
            save_chart("price_distribution.png")
            generated.append("price_distribution.png")

            plt.figure(figsize=(8.5, 5.5))
            sns.boxplot(x=prices)
            plt.title("Book Price Spread and Potential Outliers")
            plt.xlabel("Price (£)")
            save_chart("price_boxplot.png")
            generated.append("price_boxplot.png")

    if "Rating_Stars" in df.columns:
        df["Rating_Stars"] = pd.to_numeric(df["Rating_Stars"], errors="coerce")
        ratings = df["Rating_Stars"].dropna()
        if not ratings.empty:
            counts = ratings.astype(int).value_counts().sort_index()
            plt.figure(figsize=(8.5, 5.5))
            ax = sns.barplot(x=counts.index.astype(str), y=counts.values)
            ax.bar_label(ax.containers[0])
            plt.title("Number of Books by Star Rating")
            plt.xlabel("Rating (stars)")
            plt.ylabel("Number of Books")
            save_chart("rating_counts.png")
            generated.append("rating_counts.png")

    if {"Price_GBP", "Rating_Stars"}.issubset(df.columns):
        pair = df[["Price_GBP", "Rating_Stars"]].dropna()
        if not pair.empty:
            plt.figure(figsize=(8.5, 5.5))
            sns.scatterplot(data=pair, x="Rating_Stars", y="Price_GBP", alpha=0.8)
            plt.title("Book Price vs. Star Rating")
            plt.xlabel("Rating (stars)")
            plt.ylabel("Price (£)")
            save_chart("price_vs_rating.png")
            generated.append("price_vs_rating.png")

    if "Availability" in df.columns:
        availability = df["Availability"].fillna("Missing").astype(str).value_counts()
        if not availability.empty:
            plt.figure(figsize=(9, 5.5))
            ax = sns.barplot(x=availability.index, y=availability.values)
            ax.bar_label(ax.containers[0])
            plt.title("Book Availability in the Dataset")
            plt.xlabel("Availability")
            plt.ylabel("Number of Books")
            plt.xticks(rotation=20, ha="right")
            save_chart("availability_counts.png")
            generated.append("availability_counts.png")

    if not generated:
        raise SystemExit("No charts were created. Check whether the CSV has Price_GBP, Rating_Stars, or Availability columns.")

    print("CODEALPHA TASK 3 — DATA VISUALIZATION")
    print("====================================")
    print(f"Rows analyzed: {len(df)}")
    print(f"Charts generated: {len(generated)}")
    for name in generated:
        print(f" - outputs/charts/{name}")
    print("\nInterpretation tips:")
    print("- Histogram: shows the distribution of book prices.")
    print("- Box plot: highlights spread and potential price outliers for review.")
    print("- Rating bar chart: compares the number of books at each rating.")
    print("- Scatter plot: explores price-rating association, not causation.")
    print("- Availability chart: summarizes stock labels present in the CSV.")

if __name__ == "__main__":
    main()
