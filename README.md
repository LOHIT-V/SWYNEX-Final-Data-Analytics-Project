# SWYNEX Final Data Analytics Project

**Project:** Retail Sales Performance Analysis and Interactive Business Intelligence Dashboard  
**Student:** Lohit V. |

This repository contains the final retail analytics project, including the raw and cleaned datasets, reproducible Python analysis, generated charts, a written project report, and an interactive Streamlit dashboard.

## Project contents

- `PROJECT-REPORT.md` — complete project report covering all six required Task 4 components.
- `analysis.py` — reproducible Pandas analysis and chart generation.
- `app.py` — interactive Streamlit dashboard.
- `requirements.txt` — Python package dependencies.
- `data/retail_store_sales_raw.csv` — original source dataset.
- `data/SWYNEX-cleaned-retail-sales.csv` — cleaned dataset used for analysis.
- `outputs/` — generated charts and summary metrics.

## Dataset source

Retail Store Sales — Raw Dataset: https://github.com/Maichel25/retail-sales-data-cleaning/blob/main/retail_store_sales.csv


## Run locally

```bash
pip install -r requirements.txt
python analysis.py
python -m streamlit run app.py
```

## Main results

- 12,575 records across 11 columns.
- 11,971 transactions have a recorded `Total Spent` value.
- Total recorded sales: 1,552,071.00.
- Average transaction value: 129.65.
- Highest category by recorded sales: Butchers (208,118.00).
- Highest location by recorded sales: Online (791,401.00).

The 604 rows with missing `Total Spent` are excluded from sales calculations, not treated as zero. The dataset does not contain cost data, so the project reports sales rather than profit. The 2025 period ends on 18 January and is incomplete.

## Task 4 coverage

1. Problem Statement — `PROJECT-REPORT.md`, Section 1.
2. Dataset Information — Section 2.
3. Cleaning Process — Section 3.
4. Analysis — Section 4.
5. Dashboard — Section 5 and `app.py`.
6. Key Business Insights — Section 6.
