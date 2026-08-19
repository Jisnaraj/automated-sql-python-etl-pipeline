import sqlite3
import pandas as pd
import numpy as np
import datetime

# ==========================================
# STEP 1: SIMULATE RAW UNCLEANED DATA INGESTION
# ==========================================
np.random.seed(101)
raw_records = 1500

raw_data = pd.DataFrame({
    'transaction_id': [f"TXN_{1000 + i}" for i in range(raw_records)],
    'customer_id': np.random.choice([f"CUST_{i:03d}" for i in range(1, 150)], size=raw_records),
    'transaction_date': np.random.choice(
        pd.date_range('2026-01-01', '2026-03-31', freq='D').astype(str), size=raw_records
    ),
    'amount': np.random.choice([25.0, 50.0, 100.0, 250.0, np.nan, -10.0], size=raw_records, p=[0.4, 0.3, 0.15, 0.10, 0.03, 0.02]),
    'region': np.random.choice(['Kochi', 'Trivandrum', 'Calicut', 'Hyderabad', None], size=raw_records, p=[0.35, 0.25, 0.20, 0.15, 0.05])
})

# Introduce intentional duplicate rows for pipeline testing
raw_data = pd.concat([raw_data, raw_data.iloc[:50]], ignore_index=True)

# ==========================================
# STEP 2: PIPELINE CLEANING & VALIDATION
# ==========================================
def clean_and_validate_pipeline(df):
    initial_count = len(df)
    
    # 1. Deduplication
    df = df.drop_duplicates(subset=['transaction_id']).copy()
    
    # 2. Filter invalid amounts and fill missing categories
    df = df[df['amount'] > 0]
    df['amount'] = df['amount'].fillna(0.0)
    df['region'] = df['region'].fillna('Unassigned')
    
    # 3. Datetime formatting
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['year_month'] = df['transaction_date'].dt.to_period('M').astype(str)
    
    final_count = len(df)
    print(f"[PIPELINE LOG] Ingested: {initial_count} rows | Dropped (Duplicates/Invalid): {initial_count - final_count} rows | Cleaned: {final_count} rows")
    return df

cleaned_df = clean_and_validate_pipeline(raw_data)

# ==========================================
# STEP 3: DATABASE LOAD & SQL KPI AGGREGATION
# ==========================================
# Initialize SQLite database (swappable for PostgreSQL/MySQL via SQLAlchemy)
conn = sqlite3.connect('enterprise_analytics.db')

# Write cleaned data to SQL Table
cleaned_df.to_sql('fact_transactions', conn, if_exists='replace', index=False)

# SQL Query for Monthly Regional KPI Aggregation
sql_kpi_query = """
SELECT 
    year_month AS reporting_month,
    region,
    COUNT(DISTINCT customer_id) AS active_customers,
    COUNT(transaction_id) AS total_transactions,
    ROUND(SUM(amount), 2) AS gross_revenue,
    ROUND(AVG(amount), 2) AS avg_transaction_value
FROM 
    fact_transactions
GROUP BY 
    year_month, region
ORDER BY 
    reporting_month ASC, gross_revenue DESC;
"""

kpi_summary_df = pd.read_sql_query(sql_kpi_query, conn)
conn.close()

# ==========================================
# STEP 4: OUTPUT REPORTING METRICS
# ==========================================
print("\n--- AUTOMATED MONTHLY KPI SUMMARY REPORT ---")
print(kpi_summary_df.head(10).to_string(index=False))