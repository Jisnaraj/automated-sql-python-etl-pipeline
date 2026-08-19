# Automated SQL & Python ETL Reporting Pipeline

An automated data extraction, cleaning, and SQL aggregation pipeline built with Python and SQLite. This project simulates raw transactional ingestion, handles missing/duplicate data anomalies, loads processed data into a relational database, and generates automated monthly KPI summaries for business reporting.

## Features
- Data Ingestion & Cleaning: Ingests raw transaction records, removes duplicates, and filters out negative or invalid values.
- Data Validation: Implements data quality assurance steps to handle missing regional tags and format timestamps.
- Relational Database Storage: Automatically creates and populates a SQLite relational database table (`fact_transactions`).
- SQL Aggregation: Runs embedded SQL queries utilizing aggregations (`COUNT DISTINCT`, `SUM`, `AVG`) and multi-level grouping (`GROUP BY year_month, region`).
- Automated Output: Exports clean monthly KPI summaries directly to CSV for executive reporting dashboards.

## File Structure
```text
automated-sql-python-etl-pipeline/
├── .gitignore
├── README.md
├── etl_pipeline.py
├── monthly_kpi_summary.csv
├── output_screenshot.png
└── requirements.txt
