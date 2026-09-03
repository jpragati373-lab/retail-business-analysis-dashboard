# Retail Business Analysis Dashboard — Demo Flow

## 1. Project Introduction

This project is an interactive Streamlit dashboard that analyzes retail sales, profit, quantity, discounts, product groupings, geography, segments, and shipping modes. I built it to turn transaction data into clear KPIs, performance comparisons, and practical business recommendations. It helps a business identify profitable areas, weak-performing areas, and possible relationships between discounting and profit. The project uses Python, Pandas, Plotly, and Streamlit.

## 2. Dashboard Demo Order

### Step 1 — Overview

- **Show:** The dashboard title, KPI cards, active filters, and overall performance view.
- **Explain:** The dashboard is filter-aware, so every result updates for the selected data.
- **Why it matters:** Decision-makers can quickly understand the current business position.

### Step 2 — Executive Summary

- **Show:** The summary KPIs, strongest areas, weak areas, and headline findings.
- **Explain:** The summary converts detailed analysis into a concise management view.
- **Why it matters:** Leaders can prioritize investigation without reviewing every record.

### Step 3 — Category Analysis

- **Show:** Sales, profit, quantity, and profitability comparisons by category and sub-category.
- **Explain:** Compare commercial performance with profitability rather than relying only on sales.
- **Why it matters:** A high-sales category may not always be the most profitable.

### Step 4 — Regional Analysis

- **Show:** Regional, state, and city performance tables and charts.
- **Explain:** Identify geographic areas with strong sales, strong profit, or weak margins.
- **Why it matters:** Geographic performance can guide market attention and operational review.

### Step 5 — Segment & Shipping Analysis

- **Show:** Segment performance, sales mix, segment-category comparisons, and shipping analysis.
- **Explain:** Compare Consumer, Corporate, and Home Office performance using sales, profit, quantity, discounts, and margins.
- **Why it matters:** The business can understand which segments and shipping modes deserve focus.

### Step 6 — Profitability & Discount Analysis

- **Show:** Profitability KPIs, discount-versus-profit scatter chart, discount ranges, and loss-making analysis.
- **Explain:** Review whether higher discounts appear associated with weaker profitability in the filtered data.
- **Why it matters:** Discount decisions should support profitable growth, not only higher sales volume.

### Step 7 — Performance Ranking

- **Show:** Selectable rankings for categories, sub-categories, regions, and states.
- **Explain:** Rankings use sales, profit, margin, discount, and performance status to distinguish strong and weak areas.
- **Why it matters:** Teams can focus limited time on the highest-priority performers and problem areas.

### Step 8 — Business Insights

- **Show:** Dynamic insights, Business Health status, and recommendations.
- **Explain:** These statements are calculated from the active filtered dataset rather than hard-coded.
- **Why it matters:** Analysis becomes actionable by connecting patterns to possible business decisions.

### Step 9 — Data Explorer

- **Show:** Search, column selection, sorting, data-quality information, and CSV downloads.
- **Explain:** Users can inspect the underlying filtered records and export results for further work.
- **Why it matters:** Transparency and self-service exploration improve trust in the analysis.

## 3. Sample Interview Script

“I developed a Retail Business Analysis Dashboard to analyze transaction-level retail performance. The goal was to help users understand not only where sales are generated, but also where profit is created or lost.

The dataset includes sales, profit, quantity, discount, category, sub-category, region, state, city, segment, and shipping information. I used Python and Pandas to validate the data, convert numeric fields, apply filters, calculate KPIs, and create grouped summaries. Plotly provides interactive charts, while Streamlit turns the analysis into a user-friendly dashboard.

The dashboard includes an Executive Summary, category and regional analysis, segment and shipping analysis, profitability and discount analysis, performance rankings, Business Insights, and a Data Explorer. Users can filter the data by several dimensions and download filtered results or a business summary.

A key focus was comparing sales with profit margin and reviewing discount ranges. The dashboard also identifies loss-making categories, sub-categories, states, and segments when they exist in the selected data. Recommendations are generated from the current results, such as reviewing excessive discounting or investigating weak profitability. I also included data-quality reporting and safeguards for missing values, empty results, and zero sales.”

## 4. Business Questions

1. Which category generates the most sales?
2. Which category generates the most profit?
3. Which sub-categories have the strongest and weakest profitability?
4. Which region performs best by sales, profit, or profit margin?
5. Which states have weak or negative profitability?
6. Which cities generate the highest sales and profit?
7. Does higher discounting appear associated with lower profit?
8. Which customer segment contributes the most sales or profit?
9. How does performance differ across shipping modes?
10. Which discount range has the strongest or weakest profitability?

## 5. Technical Questions and Answers

### 1. Which programming language did you use?

I used Python because it provides strong libraries for data analysis, visualization, and dashboard development.

### 2. How did you use Pandas?

I used Pandas to load the CSV, clean numeric columns, filter records, group data, aggregate metrics, sort results, and prepare chart data.

### 3. What data-cleaning steps were important?

I validated the expected columns, converted numeric fields safely, inspected missing values and duplicates, and handled invalid or incomplete values during calculations.

### 4. How do the dashboard filters work?

Each selected sidebar value is applied sequentially to the dataframe. All KPIs, charts, tables, insights, and downloads use the filtered dataframe.

### 5. How did you use GroupBy?

I grouped records by dimensions such as Category, Region, Segment, State, City, and Sub-Category to calculate sales, profit, quantity, discount, and record counts.

### 6. Which aggregations did you calculate?

I used sums for sales, profit, and quantity; means for discount and selected per-record metrics; counts for records; and derived margins from aggregated sales and profit.

### 7. How is profit margin calculated?

Profit margin is calculated as total profit divided by total sales, multiplied by 100. The code safely handles zero sales.

### 8. Why did you use Plotly?

Plotly provides interactive charts with hover information, readable axes, and responsive comparisons across business dimensions.

### 9. Why did you use Streamlit?

Streamlit allowed me to present the analysis as an interactive application with filters, KPI cards, tables, expanders, and downloads.

### 10. How does CSV export work?

The dashboard converts the current filtered or summarized dataframe to CSV and provides it through Streamlit download buttons.

## 6. Challenges

- Working within the dataset's available fields without adding customer-level or date-level analysis.
- Handling missing or invalid numeric values during KPI calculations.
- Keeping all charts, tables, insights, and downloads synchronized with multiple filters.
- Displaying clear messages when filters return no records.
- Avoiding division-by-zero errors when sales are zero.
- Building interactive visualizations that remain readable across different filtered datasets.

## 7. Dataset Limitation

The dataset contains sales, profit, quantity, discount, category, sub-category, region, state, city, segment, and shipping information, along with country and postal code fields.

It does not contain customer-level fields such as Customer ID or Customer Name, or date-level fields such as Order Date. Therefore, the dashboard focuses on transaction-level, product, geographic, segment, shipping, profitability, and discount analysis. It cannot support customer lifetime analysis, customer retention analysis, or time-series trends unless those fields become available.

## 8. Final Presentation Tips

1. Start with the business problem, not the code.
2. Explain that all results respond to the active filters.
3. Compare profit and margin alongside sales.
4. Use one or two meaningful examples from the live dashboard.
5. Explain why discount analysis matters commercially.
6. Mention the dataset limitation honestly.
7. Show how insights lead to recommendations.
8. Finish by demonstrating the Data Explorer and CSV export.

## 9. Project Checklist

- [ ] Dashboard runs
- [ ] Filters work
- [ ] Charts work
- [ ] Executive Summary works
- [ ] Business Insights work
- [ ] Data Explorer works
- [ ] CSV download works
- [ ] README complete
- [ ] requirements.txt complete
- [ ] .gitignore complete
- [ ] GitHub repository ready

**PROJECT DEVELOPMENT: COMPLETE**  
**PROJECT PRESENTATION: READY**
