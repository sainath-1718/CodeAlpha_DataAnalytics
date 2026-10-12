# CodeAlpha Data Analytics Internship — Task 1: Web Scraping

**Project:** Books and Prices Dataset  
**Domain:** Data Analytics  
**Tools:** Python, Requests, BeautifulSoup, pandas  
**Practice source:** https://books.toscrape.com/

## 1. Objective
Automatically collect book titles, listed prices, star ratings, availability text, and product URLs from a public practice catalogue, then save the results as a CSV dataset.

## 2. Why this project?
Manually copying book information is repetitive and error-prone. A small Python scraper demonstrates how to retrieve HTML, parse relevant elements, structure records, and export data for later analysis.

## 3. Dataset fields
| Column | Description |
|---|---|
| `Book_Name` | Book title |
| `Price_GBP` | Listed price in pounds sterling |
| `Rating_Stars` | Rating from 1 to 5 stars |
| `Availability` | Availability text shown on the page |
| `Product_URL` | Product detail page URL |

## 4. Project structure
```text
CodeAlpha_Web_Scraping_Books/
├── data/
│   └── books_dataset_sample.csv
├── reports/
│   └── project_report.md
├── src/
│   └── scrape_books.py
├── requirements.txt
└── README.md
```

## 5. Setup
Use Python 3.10 or newer.

```bash
python -m venv .venv
```

Activate the environment:

- **Windows PowerShell:** `.venv\Scripts\Activate.ps1`
- **Windows CMD:** `.venv\Scripts\activate.bat`
- **macOS/Linux:** `source .venv/bin/activate`

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## 6. Run the scraper
From the project root:

```bash
python src/scrape_books.py --pages 2
```

The script saves live results to `data/books_dataset.csv`. You can choose more pages (up to 50) with `--pages`, but use reasonable request intervals and follow the website's terms and access rules.

To choose a custom output path:

```bash
python src/scrape_books.py --pages 3 --output data/my_books.csv
```

## 7. Offline sample data
`data/books_dataset_sample.csv` is included as an example so you can inspect the expected columns without internet access. **It is sample/example data, not a fresh scrape performed during packaging.** Run the script to collect current live records.

## 8. Methodology
1. Send an HTTP GET request to the practice catalogue.
2. Parse the HTML using BeautifulSoup.
3. Select book cards with `article.product_pod`.
4. Extract title, price, rating, availability, and product URL.
5. Convert the price to a numeric value and rating to a 1–5 integer.
6. Remove duplicate product URLs.
7. Export the records to CSV and print a basic quality summary.

## 9. Validation
The script reports record count, columns, missing values, duplicate product URLs, and minimum/maximum/average prices. Live results can vary as the website changes or becomes unavailable.

## 10. Responsible scraping
- Use a practice/public source and check its terms and `robots.txt`.
- Make requests at a modest rate; this project waits one second between pages.
- Do not bypass logins, CAPTCHAs, paywalls, rate limits, or other access controls.
- Do not collect personal or sensitive data.
- Stop if the website disallows the activity or returns access-denied responses.

## 11. Internship submission checklist
- [ ] Run the script and generate `data/books_dataset.csv`.
- [ ] Verify the CSV opens correctly.
- [ ] Add screenshots of successful execution and sample CSV rows to your project documentation.
- [ ] Upload the complete project to a GitHub repository named `CodeAlpha_Web_Scraping_Books`.
- [ ] Share a short video explanation on LinkedIn with the repository link, as requested in the supplied internship instructions.
- [ ] Submit the task through the submission form shared by CodeAlpha.

## 12. Important note
The supplied CodeAlpha instructions say interns must complete at least two tasks (or three, as applicable to the program instructions); one task alone is considered incomplete for certificate eligibility. Confirm the exact minimum with your internship coordinator if unclear.
