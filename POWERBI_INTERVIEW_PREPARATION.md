# Power BI Interview Preparation — Retail Data Analyst

This module uses the project's actual retail fields:

`Ship Mode`, `Segment`, `Country`, `City`, `State`, `Postal Code`, `Region`, `Category`, `Sub-Category`, `Sales`, `Quantity`, `Discount`, and `Profit`.

It does not assume Order Date, Customer ID, Customer Name, or Product Name.

## 1. Power BI Fundamentals

- **Power BI:** Microsoft's business intelligence platform for connecting to data, transforming it, modeling it, and creating interactive reports.
- **Power BI Desktop:** The Windows application used to import data, use Power Query, create relationships, write DAX, and design reports.
- **Power BI Service:** The cloud platform used to publish, share, refresh, and collaborate on reports.
- **Power BI Report:** A collection of interactive report pages containing visuals, filters, and analysis.
- **Dashboard vs Report:** A dashboard is usually a single-page monitoring view made from pinned tiles; a report can contain multiple interactive pages.
- **Dataset/Semantic Model:** The prepared data and model used by a report. In current Power BI terminology, “semantic model” is commonly used instead of dataset.
- **Data Model:** Tables, columns, measures, and relationships that define how the data behaves.
- **Workspace:** A collaborative area in Power BI Service where reports, semantic models, dashboards, and apps are managed.

## 2. Power BI Data Import

### CSV

In Power BI Desktop, choose **Home → Get data → Text/CSV**, select the file, preview it, and choose **Transform Data** or **Load**.

CSV is useful for flat transaction exports such as the project's `SampleSuperstore.csv`.

### Excel

Choose **Home → Get data → Excel**, select the workbook and worksheet or table, then transform or load it.

Excel is useful when business users maintain structured worksheets or multiple related tables.

### SQL Server or MySQL

Choose **Get data**, select the database connector, enter the server and database details, authenticate, and choose Import or DirectQuery.

Database sources are useful for larger, regularly updated, governed business data.

## 3. Power Query

**Power Query** is the data preparation layer in Power BI. It applies repeatable transformation steps before data reaches the model.

Common examples:

- **Remove duplicates:** Select columns or the whole table, then choose **Remove Rows → Remove Duplicates**.
- **Replace values:** Replace inconsistent labels, such as changing `West ` to `West`.
- **Change data types:** Set `Sales`, `Quantity`, `Discount`, and `Profit` to suitable numeric types.
- **Handle null values:** Replace, remove, or preserve nulls depending on the business meaning.
- **Split columns:** Split a combined location field by a delimiter, if such a field exists.
- **Merge columns:** Combine existing text fields into a display label, if useful.
- **Append queries:** Stack tables with the same structure, such as monthly files. This project does not have date-based files.
- **Filter rows:** Remove invalid records or keep only required values.

Example workflow for this project:

1. Import `SampleSuperstore.csv`.
2. Confirm the 13 expected columns.
3. Set numeric types for sales, quantity, discount, and profit.
4. Review nulls and duplicate rows.
5. Trim text values and standardize category labels if needed.
6. Close and apply the query.

## 4. Data Modeling

- **Relationship:** A connection between tables based on related columns.
- **One-to-one:** One row in table A matches one row in table B.
- **One-to-many:** One dimension row, such as one category, relates to many fact rows.
- **Many-to-many:** Multiple rows on both sides can match; it requires careful modeling.
- **Primary key:** A unique identifier in a table.
- **Foreign key:** A column that references a key in another table.
- **Fact table:** A table containing measurable business events, such as sales transactions.
- **Dimension table:** A descriptive table containing categories such as region or segment.
- **Star schema:** A central fact table connected directly to dimension tables.

Good modeling matters because it improves filter behavior, reduces ambiguity, supports reusable measures, and makes reports easier to maintain. For this single-table dataset, a simple imported model is sufficient. In a larger implementation, the transaction table could be separated from validated category, geography, segment, and shipping dimensions.

## 5. DAX

Assume the table is named `RetailData`.

```DAX
Total Sales = SUM(RetailData[Sales])

Average Sales = AVERAGE(RetailData[Sales])

Record Count = COUNT(RetailData[Sales])

Distinct States = DISTINCTCOUNT(RetailData[State])

Total Profit = SUM(RetailData[Profit])

Profit Margin = DIVIDE([Total Profit], [Total Sales], 0)

Profitable Sales =
CALCULATE(
    [Total Sales],
    FILTER(RetailData, RetailData[Profit] > 0)
)

Profitability Status =
IF([Profit Margin] >= 0.20, "Strong",
   IF([Profit Margin] >= 0.10, "Healthy", "Needs attention"))

Total Quantity = SUM(RetailData[Quantity])

Average Profit = AVERAGE(RetailData[Profit])
```

Additional examples using generic related tables:

```DAX
Weighted Profit = SUMX(RetailData, RetailData[Sales] - RetailData[Discount])

Category Name = RELATED(CategoryDimension[CategoryName])
```

`SUMX()` evaluates an expression row by row and then sums the results. `RELATED()` retrieves a value from a related table through an established relationship.

### Calculated Column vs Measure

- **Calculated column:** Computed for every row during data refresh. It is stored in the model and can be used for categories, filtering, and row-level logic.
- **Measure:** Computed when a visual is evaluated. It responds to slicers and filter context and is usually preferred for KPIs.

For totals and profit margin, measures are generally the better choice because they update dynamically with filters.

## 6. KPI Development

Recommended measures:

```DAX
Total Sales = SUM(RetailData[Sales])

Total Profit = SUM(RetailData[Profit])

Total Quantity = SUM(RetailData[Quantity])

Profit Margin = DIVIDE([Total Profit], [Total Sales], 0)

Average Sales = AVERAGE(RetailData[Sales])

Average Profit = AVERAGE(RetailData[Profit])
```

Place these measures in Card visuals. Format sales and profit as currency, quantity as a whole number, and profit margin as a percentage. `DIVIDE()` is safer than the `/` operator because it handles a zero denominator.

## 7. Visualizations

| Visual | Purpose | Best use case | Common mistake |
|---|---|---|---|
| Bar chart | Compare categories horizontally | Long category or state names | Showing too many categories without sorting |
| Column chart | Compare values vertically | Sales or profit by category | Crowding labels |
| Line chart | Show change over an ordered axis | Generic date-based analysis | Using it without a meaningful time or sequence field |
| Pie/Donut chart | Show part-to-whole composition | Segment sales mix with few segments | Using too many slices or comparing close values |
| Card | Display one KPI | Total sales, profit, or margin | Showing a KPI without context |
| Table | Show exact row-level or grouped values | State or sub-category rankings | Adding too many columns |
| Matrix | Show hierarchical summaries | Category and sub-category | Creating confusing drill levels |
| Scatter plot | Compare two numeric measures | Discount versus profit | Assuming correlation proves causation |
| Map | Show geographic patterns | State or city performance | Using inaccurate locations or too many points |
| Slicer | Let users select values | Region, category, segment, or ship mode | Adding too many slicers without organization |

## 8. Interactive Dashboards

- **Slicers:** Visible controls for selecting values such as Category or Region.
- **Filters:** Restrictions applied at visual, page, or report level.
- **Drill-down:** Move from a hierarchy level, such as Category to Sub-Category.
- **Drill-through:** Open a detail page filtered to the selected item.
- **Tooltips:** Extra context shown when hovering over a visual.
- **Bookmarks:** Saved report states used for navigation or alternate views.
- **Buttons:** Interactive controls for navigation, bookmarks, or actions.
- **Cross-filtering:** Selecting one visual filters or highlights related visuals.

## 9. Retail Dashboard Design

### KPI Cards

- Total Sales
- Total Profit
- Profit Margin
- Total Quantity
- Average Discount
- Record Count

### Recommended Charts

- Sales and profit by Category
- Profit margin by Category
- Sales and profit by Region
- Profit by State
- Sales mix by Segment
- Sales and profit by Ship Mode
- Discount versus Profit scatter plot
- Quantity by Category, Region, and Segment

### Recommended Slicers

- Segment
- Category
- Sub-Category
- Region
- State
- Ship Mode

### Recommended Tables

- Category profitability table
- Regional profitability table
- State and city rankings
- Sub-category profit ranking
- Discount-range summary

### Business Insights

Use measures and rankings to identify the highest-profit category, strongest region, weakest sub-category, loss-making states, segment performance, and discount levels associated with weaker profitability. These should be calculated from the selected data, not hard-coded.

## 10. Power BI Interview Questions

### Beginner

1. **What is Power BI?**  
   It is a platform for connecting to data, modeling it, and creating interactive business reports.
2. **What is Power BI Desktop used for?**  
   It is used to build queries, models, DAX measures, and report pages.
3. **What is Power BI Service?**  
   It is the cloud environment for publishing, sharing, refreshing, and collaborating on reports.
4. **What is a report?**  
   A report is one or more interactive pages containing visuals and filters.
5. **What is a slicer?**  
   A visual filter that lets users select values.
6. **What is Power Query?**  
   It is the tool used to import and transform data before modeling.
7. **What is DAX?**  
   Data Analysis Expressions is the formula language used for measures and calculated columns.
8. **What is a measure?**  
   A dynamic calculation evaluated in the current filter context.
9. **What is a relationship?**  
   A connection between tables using related key columns.
10. **What is a card visual?**  
    A visual designed to show one important number.

### Intermediate

11. **Power Query or DAX for cleaning?**  
    Use Power Query for data preparation and DAX for model calculations and business logic.
12. **Why is a star schema useful?**  
    It creates a clear fact-and-dimension structure with predictable filtering.
13. **What does `CALCULATE()` do?**  
    It evaluates an expression after changing its filter context.
14. **Why use `DIVIDE()`?**  
    It handles zero or blank denominators more safely than direct division.
15. **What is filter context?**  
    The set of filters from slicers, visuals, pages, and relationships affecting a measure.
16. **What is row context?**  
    The current row being evaluated, especially in calculated columns and iterator functions.
17. **What is drill-through?**  
    Navigation to a detail page filtered for the selected item.
18. **What is cross-filtering?**  
    Interaction where selecting one visual changes related visuals.
19. **How would you handle duplicates?**  
    Identify whether they are valid transactions, then remove or preserve them in Power Query based on the business rule.
20. **How would you handle nulls?**  
    Understand their meaning, then replace, remove, or preserve them consistently.

### Advanced

21. **What is the difference between a measure and a calculated column?**  
    A measure is dynamic at query time; a calculated column is stored per row after refresh.
22. **What does `FILTER()` return?**  
    A table containing rows that meet a condition.
23. **What does `SUMX()` do?**  
    It evaluates an expression for each row and aggregates the results.
24. **What is `RELATED()` used for?**  
    It retrieves a value from a related table when the relationship exists.
25. **Import versus DirectQuery?**  
    Import stores data in the model for speed; DirectQuery sends queries to the source for fresher data.
26. **How would you optimize a slow report?**  
    Reduce unnecessary columns, use a star schema, simplify DAX, limit high-cardinality visuals, and inspect performance metrics.
27. **What is row-level security?**  
    A model feature that restricts which rows each user can see.
28. **Why can many-to-many relationships be risky?**  
    They can create ambiguous filter paths or unexpected totals if not modeled carefully.
29. **What is incremental refresh?**  
    A strategy that refreshes recent partitions instead of reloading all historical data.
30. **How would you validate a Power BI report?**  
    Reconcile totals with the source, test slicers, check measures at different grains, and validate edge cases such as blanks and zero sales.

## 11. Important Comparisons

| Comparison | Explanation |
|---|---|
| Power BI vs Excel | Excel is excellent for spreadsheet analysis; Power BI is stronger for governed, interactive, shareable dashboards. |
| Power BI vs Tableau | Both support visual analytics; Power BI integrates closely with Microsoft tools, while Tableau is known for flexible visual exploration. |
| Power Query vs DAX | Power Query transforms data before loading; DAX calculates model results after loading. |
| Measure vs Calculated Column | Measures respond to filter context; columns are calculated and stored row by row. |
| Dashboard vs Report | A dashboard is generally a single-page monitoring view; a report can contain multiple interactive pages. |
| Import vs DirectQuery | Import is usually faster after refresh; DirectQuery queries the source and can support fresher data. |
| Star Schema vs Snowflake Schema | Star schemas keep dimensions denormalized and simple; snowflake schemas normalize dimensions into more related tables. |
| Calculated Column vs Measure | Use a column for row-level labels or grouping; use a measure for dynamic totals, ratios, and KPIs. |

## 12. Practical Interview Questions

### 1. A manager wants to know which category generates the highest profit. How would you build the report?

Create a `Total Profit` measure, place Category on the axis of a sorted bar chart, add the measure as values, and include a card or table for the top result. Add slicers so the ranking responds to selected filters.

### 2. How would you show whether high discounts are associated with weak profit?

Use a scatter plot with Discount on the X-axis and Profit on the Y-axis, add Category or Sub-Category as a legend, and provide tooltips. Explain that the chart shows association, not causation.

### 3. How would you compare regions fairly?

Show total sales and profit by Region, then calculate profit margin with `DIVIDE([Total Profit], [Total Sales], 0)`. Comparing both absolute and relative measures avoids relying only on scale.

### 4. A report has duplicate transactions. What would you do?

Profile the duplicates in Power Query, confirm whether repeated rows are valid business records, and remove only confirmed duplicates.

### 5. How would you build a segment sales mix?

Create a Total Sales measure, place Segment in a donut chart, and format the visual to show each segment's percentage of total sales.

### 6. How would you find the weakest sub-categories?

Create a table with Sub-Category, Sales, Profit, Discount, and Profit Margin, sort by profit ascending, and conditionally format negative or low values.

### 7. How would you make a state detail page?

Create a drill-through page with State as the drill-through field, add state KPIs, charts, and a detailed table, and enable navigation from a state visual.

### 8. How would you handle zero sales in a margin KPI?

Use `DIVIDE([Total Profit], [Total Sales], 0)` and document how a zero denominator is represented.

### 9. How would you make the report user-friendly?

Use a small number of clear slicers, consistent titles, readable number formats, logical page navigation, tooltips, and concise insight text.

### 10. How would you validate the final dashboard?

Compare Power BI totals with the CSV, test each slicer in combination, inspect charts with one or no selected categories, and verify that negative profits and missing values display correctly.

## 13. Project Discussion

### How to describe the existing project

“I built an interactive retail analytics dashboard using Python, Pandas, Plotly, and Streamlit. It analyzes sales, profit, quantity, discounts, categories, geography, segments, and shipping modes. The dashboard provides dynamic KPIs, interactive filters, profitability analysis, rankings, business insights, recommendations, data-quality reporting, and CSV exports.”

### How to recreate the analysis in Power BI

1. Import `SampleSuperstore.csv` with Power Query.
2. Validate column names and set numeric data types.
3. Inspect missing values and duplicates.
4. Create a simple model or a star schema if additional validated tables become available.
5. Create DAX measures for sales, profit, quantity, average discount, and profit margin.
6. Build report pages for overview, category, regional, segment, shipping, profitability, rankings, and data exploration.
7. Add slicers for Segment, Category, Sub-Category, Region, State, and Ship Mode.
8. Add tooltips, drill-through, conditional formatting, and clear business descriptions.
9. Validate totals and filters against the Python dashboard.
10. Publish the report to Power BI Service when sharing and refresh requirements are defined.

## 14. Quick Revision Cheat Sheet

### Important terms

- Power BI Desktop: Build and model reports.
- Power BI Service: Publish and share reports.
- Power Query: Import and transform data.
- DAX: Create calculations.
- Measure: Dynamic KPI.
- Calculated column: Stored row-level calculation.
- Slicer: Visible filter.
- Relationship: Link between tables.
- Star schema: Fact table connected to dimensions.
- Filter context: Filters affecting a measure.

### Important DAX

```DAX
SUM()
AVERAGE()
COUNT()
DISTINCTCOUNT()
CALCULATE()
FILTER()
IF()
DIVIDE()
SUMX()
RELATED()
```

### Important visuals

- Cards for KPIs
- Bar or column charts for comparisons
- Donut charts for simple composition
- Scatter plots for numeric relationships
- Tables and matrices for exact detail
- Slicers for user selections

### Interview reminders

- Clean data in Power Query.
- Use measures for filter-aware KPIs.
- Use `DIVIDE()` for safe ratios.
- Validate totals against the source.
- Compare profit margin as well as total profit.
- Do not claim causation from a scatter plot alone.
- Keep dashboards focused and easy to scan.
- Respect the dataset scope: no customer-level or date-level analysis is supported here.

**POWER BI INTERVIEW MODULE: COMPLETE**
