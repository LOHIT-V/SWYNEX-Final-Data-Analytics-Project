"""Interactive Streamlit dashboard for the SWYNEX retail sales project."""
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'SWYNEX-cleaned-retail-sales.csv'
st.set_page_config(page_title='SWYNEX | Retail Sales Analytics', page_icon='📊', layout='wide')
st.title('Retail Sales Performance Dashboard')
st.caption('SWYNEX Final Data Analytics Project | Retail Store Sales dataset')

@st.cache_data
def load_data():
    d = pd.read_csv(DATA)
    d['Transaction Date'] = pd.to_datetime(d['Transaction Date'], errors='coerce')
    d['Year'] = d['Transaction Date'].dt.year.astype('Int64').astype(str)
    d['Month'] = d['Transaction Date'].dt.to_period('M').astype(str)
    return d

df = load_data()
st.sidebar.header('Dashboard Filters')
def options(col): return sorted(df[col].dropna().astype(str).unique().tolist())
categories = st.sidebar.multiselect('Product category', options('Category'), default=options('Category'))
locations = st.sidebar.multiselect('Purchase location', options('Location'), default=options('Location'))
payments = st.sidebar.multiselect('Payment method', options('Payment Method'), default=options('Payment Method'))
years = st.sidebar.multiselect('Year', options('Year'), default=options('Year'))
filtered = df[df['Category'].astype(str).isin(categories) & df['Location'].astype(str).isin(locations) & df['Payment Method'].astype(str).isin(payments) & df['Year'].isin(years)].copy()
valid = filtered.dropna(subset=['Total Spent']).copy()
sales = float(valid['Total Spent'].sum())
count = len(valid)
avg = float(valid['Total Spent'].mean()) if count else 0
customers = int(filtered['Customer ID'].nunique())

c1,c2,c3,c4 = st.columns(4)
c1.metric('Recorded sales', f'{sales:,.2f}')
c2.metric('Transactions with sales', f'{count:,}')
c3.metric('Average transaction value', f'{avg:,.2f}')
c4.metric('Unique customers', f'{customers:,}')
st.caption(f'{len(filtered):,} filtered rows | {filtered["Total Spent"].isna().sum():,} rows excluded from sales metrics because Total Spent is missing')

if valid.empty:
    st.warning('No transactions match the selected filters. Adjust the filters to view results.')
else:
    left,right = st.columns(2)
    cat = valid.groupby('Category', as_index=False)['Total Spent'].sum().sort_values('Total Spent', ascending=False)
    loc = valid.groupby('Location', as_index=False)['Total Spent'].sum().sort_values('Total Spent', ascending=False)
    pay = valid.groupby('Payment Method', as_index=False)['Total Spent'].sum().sort_values('Total Spent', ascending=False)
    month = valid.groupby('Month', as_index=False)['Total Spent'].sum().sort_values('Month')
    with left: st.plotly_chart(px.bar(cat, x='Category', y='Total Spent', title='Sales by Product Category'), width='stretch')
    with right: st.plotly_chart(px.bar(loc, x='Location', y='Total Spent', title='Sales by Purchase Location'), width='stretch')
    with left: st.plotly_chart(px.pie(pay, names='Payment Method', values='Total Spent', title='Sales by Payment Method'), width='stretch')
    with right: st.plotly_chart(px.line(month, x='Month', y='Total Spent', markers=True, title='Monthly Recorded Sales'), width='stretch')
    st.subheader('Key insights for the current filters')
    top_cat = cat.sort_values('Total Spent', ascending=False).iloc[0]
    top_loc = loc.sort_values('Total Spent', ascending=False).iloc[0]
    top_pay = pay.sort_values('Total Spent', ascending=False).iloc[0]
    year_sales = valid.groupby('Year', as_index=False)['Total Spent'].sum().sort_values('Total Spent', ascending=False)
    top_year = year_sales.iloc[0]
    st.write(f'- **Top category by recorded sales:** {top_cat["Category"]} ({top_cat["Total Spent"]:,.2f}).')
    st.write(f'- **Top purchase location:** {top_loc["Location"]} ({top_loc["Total Spent"]:,.2f}).')
    st.write(f'- **Top payment method by recorded sales:** {top_pay["Payment Method"]} ({top_pay["Total Spent"]:,.2f}).')
    st.write(f'- **Highest-sales year in the current selection:** {top_year["Year"]} ({top_year["Total Spent"]:,.2f}).')
    st.write(f'- **Average recorded transaction value:** {avg:,.2f} across {count:,} transactions.')
    st.subheader('Filtered transaction sample')
    st.caption('Showing up to 100 matching transactions as a preview.')
    st.dataframe(filtered.head(100), width='stretch')

with st.expander('Data quality and interpretation notes'):
    st.markdown('''
    - The source contains 12,575 transaction rows and 11 columns.
    - 604 rows have both `Quantity` and `Total Spent` missing. They are retained in the dataset but excluded from sales totals and average transaction value.
    - The `Item` and `Discount Applied` fields contain the `Unknown` label where the earlier cleaning process replaced missing values.
    - The dataset has no cost or expense fields; therefore, the dashboard reports **recorded sales**, not profit or profitability.
    - The available dates run from 1 January 2022 to 18 January 2025. The 2025 period is partial and should not be compared with complete years as if it were a full year.
    - High-value transactions are not automatically removed. They should be checked against source records before any exclusion.
    ''')
