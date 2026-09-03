# Retail Business Analysis Dashboard

Interactive retail analytics dashboard built with Python, Pandas, Plotly, and Streamlit. It analyzes transaction-level sales, profit, quantity, discounts, categories, regions, states, cities, segments, and shipping modes. The dashboard supports evidence-based KPI monitoring, profitability review, performance ranking, and commercial decision-making.

**GitHub description:** Interactive retail analytics dashboard built with Python, Pandas, Plotly and Streamlit for KPI, profitability and business performance analysis.

## 🚀 Live Dashboard

[View Live Dashboard](YOUR_LIVE_STREAMLIT_URL)

Explore the interactive retail analytics dashboard to analyze sales, profitability, discounts, categories, regions, segments, and business performance.

## Project Highlights

- Interactive KPI dashboard
- Dynamic filters
- Category and sub-category analysis
- Regional and state analysis
- Segment and shipping analysis
- Profitability and discount analysis
- Performance rankings
- Business insights and recommendations
- Data Explorer and CSV exports

## Key Highlights

- Interactive Streamlit dashboard with responsive layouts and filter-aware analysis
- Business KPI and profitability analysis using sales, profit, quantity, and margin
- Discount impact analysis with range comparisons and discount/profit relationships
- Regional, category, sub-category, state, city, segment, and shipping performance analysis
- Dynamic Executive Summary, Business Insights, and recommendations
- Performance rankings and Business Health indicators
- Data Quality Report, searchable Data Explorer, and CSV export functionality

## Project Overview

The dashboard analyzes retail sales, profitability, quantity, discounts, categories, sub-categories, regions, states, cities, customer segments, and shipping modes. Every displayed result is calculated from the supplied dataset and updates when sidebar filters change.

## Dashboard Preview

Add captured dashboard images to the `screenshots/` folder using these filenames:

- `screenshots/dashboard-overview.png`
- `screenshots/category-analysis.png`
- `screenshots/regional-analysis.png`
- `screenshots/profitability-analysis.png`

The image paths above are intentional placeholders. No screenshots are included until they are captured from the running dashboard.

## Screenshots

These screenshots should demonstrate:

- Dashboard overview and KPI cards
- Category and sub-category analysis
- Regional and state performance
- Profitability and discount analysis
- Business insights and recommendations

## Why This Project Matters

This project demonstrates how raw retail transaction data can be transformed into transparent KPIs, visual analysis, business insights, and actionable recommendations. It focuses on measurable analytical workflows without claiming unmeasured real-world business impact.

## Recruiter Summary

- Evaluates practical Python and Pandas skills for cleaning and summarizing transaction data.
- Demonstrates exploratory data analysis across product groupings, geography, segments, shipping, and discounts.
- Shows data visualization capability through interactive Plotly charts and a Streamlit dashboard.
- Highlights business analysis through dynamic KPIs, recommendations, data-quality reporting, and exports.

## Business Objective

The project helps answer practical business questions:

- Which categories and sub-categories generate the strongest sales and profit?
- Which regions, states, and cities require attention?
- How do customer segments and shipping modes contribute to performance?
- Are higher discounts associated with weaker profitability?
- Where should management focus commercial and operational action?

## Key Features

- Interactive KPI dashboard
- Sidebar filtering by Segment, Category, Sub-Category, Region, State, and Ship Mode
- Category and sub-category analysis
- Regional, state, and city analysis
- Segment and shipping analysis
- Discount vs. Profit analysis
- Profitability analysis and Business Health status
- Performance rankings with high/average/low performer labels
- Executive Summary
- Dynamic Business Insights
- Business Recommendations
- Data Explorer with search, column selection, and sorting
- Data Quality Report
- Filtered dataset and business summary CSV exports

## Dataset

The project uses `SampleSuperstore.csv` with these actual 13 columns:

- Ship Mode
- Segment
- Country
- City
- State
- Postal Code
- Region
- Category
- Sub-Category
- Sales
- Quantity
- Discount
- Profit

The dataset does not contain customer-level fields such as Customer ID or Customer Name, date-level fields such as Order Date, order identifiers, or product names. The dashboard does not invent or infer those unavailable dimensions.

## Technologies

- Python
- Pandas
- Plotly
- Streamlit

## Skills Demonstrated

**Programming**

- Python
- Pandas

**Visualization**

- Plotly
- Streamlit

**Analytics**

- Data Cleaning
- Exploratory Data Analysis (EDA)
- KPI Analysis
- Profitability Analysis
- Business Insights

**Tools**

- VS Code
- Git
- GitHub

## How to Run

These instructions are suitable for Windows and PowerShell.

1. Clone or download this repository.
2. Open the project folder in VS Code.
3. Create and activate a virtual environment if needed:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the project dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. Start the Streamlit dashboard:

   ```powershell
   streamlit run app.py
   ```

## Project Structure

```text
Retail_Business_Analysis/
├── app.py
├── Retail_Business_Analysis.py
├── SampleSuperstore.csv
├── cleaned_superstore_data.csv
├── requirements.txt
├── README.md
└── .gitignore
```

- `app.py` is the interactive Streamlit dashboard.
- `Retail_Business_Analysis.py` contains the standalone analysis workflow.
- `SampleSuperstore.csv` is the source dataset.
- `cleaned_superstore_data.csv` is an optional cleaned-data output retained for reproducible analysis.
- Local report text files, chart output folders, virtual environments, caches, and IDE files are excluded by `.gitignore`.

## Business Insights

The dashboard generates filter-aware insights such as the highest-sales and highest-profit categories, strongest and weakest regions, loss-making sub-categories or states, and the observed relationship between discount and profit. No business result is hard-coded; conclusions are derived from the active filtered data.

## Future Improvements

- Analyze larger and more varied retail datasets.
- Add customer-level analysis if validated customer fields become available.
- Add time-series analysis if validated date fields become available.
- Deploy the dashboard for wider stakeholder access.
- Add automated data refresh and scheduled quality checks.
- Add automated tests for KPI calculations and filter edge cases.

## Resume Description

- Built an interactive Streamlit dashboard to analyze retail sales, profit, quantity, discounts, and performance across multiple business dimensions.
- Used Pandas and Plotly to clean, summarize, rank, and visualize filtered transaction data through dynamic KPIs, profitability tables, and comparative charts.
- Delivered data-quality reporting, searchable exploration, CSV exports, and filter-aware business insights to support practical commercial decisions.

## Portfolio Note

This project demonstrates an end-to-end Data Analyst workflow: validate the source data, clean and summarize it with Pandas, communicate patterns through Plotly, and deliver an interactive business tool with Streamlit.
