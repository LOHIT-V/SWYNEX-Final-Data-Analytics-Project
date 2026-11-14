"""SWYNEX Final Data Analytics Project: retail sales analysis."""
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'SWYNEX-cleaned-retail-sales.csv'
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)
df = pd.read_csv(DATA)
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')
valid = df.dropna(subset=['Total Spent']).copy()
valid['Year'] = valid['Transaction Date'].dt.year
valid['Month'] = valid['Transaction Date'].dt.to_period('M').astype(str)

# Summary metrics
q1, q3 = valid['Total Spent'].quantile([.25, .75])
iqr = q3 - q1
outlier_count = int((valid['Total Spent'] > q3 + 1.5 * iqr).sum())
summary = {
    'rows': int(len(df)), 'columns': int(len(df.columns)),
    'transactions_with_sales': int(len(valid)),
    'transactions_excluded_missing_total': int(df['Total Spent'].isna().sum()),
    'recorded_sales': round(float(valid['Total Spent'].sum()), 2),
    'average_transaction_value': round(float(valid['Total Spent'].mean()), 2),
    'median_transaction_value': round(float(valid['Total Spent'].median()), 2),
    'unique_customers': int(df['Customer ID'].nunique()),
    'duplicate_transaction_ids': int(df['Transaction ID'].duplicated().sum()),
    'potential_high_value_outliers_iqr': outlier_count,
    'date_min': str(df['Transaction Date'].min().date()),
    'date_max': str(df['Transaction Date'].max().date()),
    'category_sales': {str(k): round(float(v), 2) for k, v in valid.groupby('Category')['Total Spent'].sum().sort_values(ascending=False).items()},
    'location_sales': {str(k): round(float(v), 2) for k, v in valid.groupby('Location')['Total Spent'].sum().sort_values(ascending=False).items()},
    'payment_sales': {str(k): round(float(v), 2) for k, v in valid.groupby('Payment Method')['Total Spent'].sum().sort_values(ascending=False).items()},
    'year_sales': {str(int(k)): round(float(v), 2) for k, v in valid.groupby('Year')['Total Spent'].sum().sort_index().items()},
}
(OUT / 'summary_metrics.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')

# Consistent, reproducible chart exports
charts = [
    (valid.groupby('Category')['Total Spent'].sum().sort_values(), 'Sales by Product Category', 'Recorded sales', 'sales_by_category.png', 'barh'),
    (valid.groupby('Location')['Total Spent'].sum().sort_values(), 'Sales by Purchase Location', 'Recorded sales', 'sales_by_location.png', 'bar'),
    (valid.groupby('Payment Method')['Total Spent'].sum().sort_values(), 'Sales by Payment Method', 'Recorded sales', 'sales_by_payment_method.png', 'bar'),
    (valid.groupby('Month')['Total Spent'].sum().sort_index(), 'Monthly Recorded Sales', 'Recorded sales', 'monthly_sales_trend.png', 'line'),
]
for series, title, ylabel, filename, kind in charts:
    fig, ax = plt.subplots(figsize=(10, 5.5))
    if kind == 'barh': series.plot(kind='barh', ax=ax)
    elif kind == 'bar': series.plot(kind='bar', ax=ax)
    else: series.plot(kind='line', marker='o', ax=ax)
    ax.set_title(title); ax.set_ylabel(ylabel); ax.set_xlabel('')
    ax.grid(axis='x' if kind == 'barh' else 'y', alpha=.25)
    fig.tight_layout(); fig.savefig(OUT / filename, dpi=160); plt.close(fig)
print(json.dumps(summary, indent=2))
