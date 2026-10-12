from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "books_dataset.csv"
OUT = ROOT / "outputs"

def main():
    if not DATA.exists():
        raise SystemExit(
            f"Dataset not found: {DATA}\n"
            "Place your Task 1 books_dataset.csv in the data folder and run again."
        )

    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)
    report = [
        "CODEALPHA TASK 2 — EXPLORATORY DATA ANALYSIS",
        "=" * 48,
        "",
        "1. DATASET OVERVIEW",
        "-" * 20,
        f"Number of rows: {df.shape[0]}",
        f"Number of columns: {df.shape[1]}",
        f"Column names: {', '.join(map(str, df.columns))}",
        "",
        "2. DATA TYPES",
        "-" * 12,
        df.dtypes.to_string(),
        "",
        "3. DESCRIPTIVE STATISTICS",
        "-" * 26,
        df.describe(include="all").transpose().to_string(),
        "",
        "4. DATA QUALITY",
        "-" * 14,
        "Missing values per column:",
        df.isna().sum().to_string(),
        f"Duplicate rows: {int(df.duplicated().sum())}",
    ]

    if "Product_URL" in df.columns:
        report.append(f"Duplicate product URLs: {int(df['Product_URL'].duplicated().sum())}")

    quality = pd.DataFrame({
        "Column": df.columns,
        "Data_Type": [str(df[c].dtype) for c in df.columns],
        "Missing_Count": [int(df[c].isna().sum()) for c in df.columns],
        "Missing_Percent": [round(float(df[c].isna().mean() * 100), 2) for c in df.columns],
        "Unique_Values": [int(df[c].nunique(dropna=True)) for c in df.columns],
    })
    quality.to_csv(OUT / "data_quality.csv", index=False, encoding="utf-8-sig")

    if "Price_GBP" in df.columns:
        prices = pd.to_numeric(df["Price_GBP"], errors="coerce")
        valid_prices = prices.dropna()
        report += ["", "5. PRICE ANALYSIS (GBP)", "-" * 23]
        if not valid_prices.empty:
            report += [
                f"Valid price values: {len(valid_prices)}",
                f"Mean price: £{valid_prices.mean():.2f}",
                f"Median price: £{valid_prices.median():.2f}",
                f"Minimum price: £{valid_prices.min():.2f}",
                f"Maximum price: £{valid_prices.max():.2f}",
                f"Standard deviation: £{valid_prices.std():.2f}" if len(valid_prices) > 1 else "Standard deviation: unavailable",
            ]
            q1, q3 = valid_prices.quantile([0.25, 0.75])
            iqr = q3 - q1
            outliers = valid_prices[(valid_prices < q1 - 1.5 * iqr) | (valid_prices > q3 + 1.5 * iqr)]
            report.append(f"Potential price outliers (1.5 × IQR rule): {len(outliers)}")
            if "Book_Name" in df.columns:
                clean = pd.DataFrame({"Book_Name": df["Book_Name"], "Price_GBP": prices}).dropna()
                if not clean.empty:
                    max_row = clean.loc[clean["Price_GBP"].idxmax()]
                    min_row = clean.loc[clean["Price_GBP"].idxmin()]
                    report += [
                        f"Highest-priced book: {max_row['Book_Name']} (£{max_row['Price_GBP']:.2f})",
                        f"Lowest-priced book: {min_row['Book_Name']} (£{min_row['Price_GBP']:.2f})",
                    ]
        else:
            report.append("No valid numeric prices were found.")

    if "Rating_Stars" in df.columns:
        ratings = pd.to_numeric(df["Rating_Stars"], errors="coerce")
        report += ["", "6. RATING DISTRIBUTION", "-" * 22, ratings.value_counts(dropna=False).sort_index().to_string()]

    if {"Price_GBP", "Rating_Stars"}.issubset(df.columns):
        pair = df[["Price_GBP", "Rating_Stars"]].apply(pd.to_numeric, errors="coerce").dropna()
        report += ["", "7. PRICE AND RATING RELATIONSHIP", "-" * 32]
        if len(pair) >= 2 and pair["Price_GBP"].nunique() > 1 and pair["Rating_Stars"].nunique() > 1:
            corr = pair["Price_GBP"].corr(pair["Rating_Stars"])
            report += [
                f"Pearson correlation: {corr:.3f}",
                "Interpretation: this measures linear association in this sample; it does not prove causation.",
            ]
        else:
            report.append("Insufficient valid data or variation to calculate correlation.")

    report += [
        "",
        "8. CONCLUSION AND LIMITATIONS",
        "-" * 30,
        "The report summarizes the available scraped catalogue sample and flags basic data-quality issues.",
        "Potential outliers are review candidates, not automatically errors.",
        "The sample may not represent the complete book market. Conclusions should be limited to these records.",
    ]

    report_path = OUT / "eda_summary.txt"
    report_path.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    print(f"\nSaved report: {report_path}")
    print(f"Saved data quality file: {OUT / 'data_quality.csv'}")

if __name__ == "__main__":
    main()
