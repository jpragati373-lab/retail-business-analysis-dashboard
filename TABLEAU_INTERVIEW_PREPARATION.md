# Tableau Interview Preparation — Retail Data Analyst

This module uses the project's actual fields:

`Ship Mode`, `Segment`, `Country`, `City`, `State`, `Postal Code`, `Region`, `Category`, `Sub-Category`, `Sales`, `Quantity`, `Discount`, and `Profit`.

It does not assume Order Date, Order ID, Customer ID, Customer Name, or Product Name.

## 1. Tableau Fundamentals

- **Tableau:** A visual analytics platform for connecting to data, exploring it, and building interactive reports.
- **Tableau Desktop:** The authoring application used to connect data, create calculations, build worksheets, dashboards, and stories.
- **Tableau Cloud:** Tableau's hosted sharing and collaboration platform.
- **Tableau Server:** An organization-managed Tableau deployment hosted on its own infrastructure.
- **Workbook:** A Tableau file containing data connections, worksheets, dashboards, and stories.
- **Worksheet:** One view or visualization built from fields.
- **Dashboard:** A collection of worksheets arranged on one screen.
- **Story:** A sequence of story points used to present analysis as a narrative.
- **Data Source:** The connected file, database, or published data asset used by Tableau.
- **Marks:** Visual data points such as bars, circles, lines, or map shapes.
- **Dimensions:** Descriptive fields used to categorize data, such as Region or Category.
- **Measures:** Numeric fields that can be aggregated, such as Sales or Profit.
- **Discrete fields:** Blue pills that create headers or separate categories.
- **Continuous fields:** Green pills that create an axis or continuous range.

## 2. Connecting Data

### CSV

Choose **Connect → Text File**, select `SampleSuperstore.csv`, review the fields, and open a worksheet. CSV is useful for flat transaction exports and small portfolio datasets.

### Excel

Choose **Connect → Microsoft Excel**, select a workbook and sheet, then review the data model. Excel is useful when business users maintain structured worksheets.

### SQL databases

Choose the relevant connector, enter the server and database details, authenticate, and select tables or custom SQL. SQL sources are useful for larger, governed, frequently refreshed data.

### Live connection vs Extract

- **Live connection:** Queries the source when the view is opened or interacted with. Use it when freshness is important and the source can handle queries.
- **Extract:** Copies data into Tableau's optimized extract format. Use it for faster interaction, offline work, or when reducing source-system load matters.

## 3. Data Preparation

- **Data types:** Set Sales and Profit to numeric, Quantity to whole number, Discount to numeric, and descriptive fields to text.
- **Missing values:** Profile nulls, understand their meaning, then filter, replace, or preserve them consistently.
- **Duplicates:** Confirm whether repeated rows are valid transactions before removing them.
- **Filtering:** Restrict data at the worksheet, dashboard, or source level.
- **Renaming fields:** Use clear business labels without changing the underlying meaning.
- **Calculated fields:** Create reusable logic such as profit margin or profit status.
- **Data source filters:** Restrict records before they are available to worksheets, which can improve performance and control scope.

## 4. Dimensions and Measures

- A **dimension** describes or groups data. Examples: `Category`, `Region`, `Segment`, and `Ship Mode`.
- A **measure** is numeric and can be aggregated. Examples: `Sales`, `Profit`, `Quantity`, and `Discount`.
- **Discrete** fields create separate headers, such as one header per category.
- **Continuous** fields create an axis, such as a continuous Profit range.

For example, place `Category` on Columns and `SUM(Sales)` on Rows to create category sales bars. Use a discrete Category for separate bars and a continuous Sales measure for the axis.

## 5. Important Tableau Charts

| Chart | Purpose | Best use case | Common mistake |
|---|---|---|---|
| Bar chart | Compare categories horizontally | States or sub-categories with long names | Leaving values unsorted |
| Column chart | Compare values vertically | Sales or profit by category | Showing too many columns |
| Line chart | Show ordered change | Time series when a date field exists | Using it without a meaningful sequence |
| Area chart | Show trend and volume together | Cumulative or composition trends | Overlapping too many areas |
| Pie/Donut chart | Show part-to-whole composition | Sales mix by Segment | Using many similar slices |
| Scatter plot | Compare two numeric measures | Discount versus Profit | Treating association as causation |
| Histogram | Show distribution of one numeric field | Distribution of Discount or Profit | Using too many or too few bins |
| Heat map | Compare intensity across two dimensions | Region by Category profit | Using colors without a clear legend |
| Tree map | Show hierarchical part-to-whole | Category and Sub-Category sales | Using it for precise comparisons |
| KPI card | Show one important number | Total Sales or Profit Margin | Omitting units or context |
| Map | Show geographic patterns | State or City performance | Incorrect geographic roles |
| Table | Show exact values | Rankings and detailed metrics | Adding too many columns |
| Dual-axis chart | Compare two measures with different scales | Sales and profit margin | Misleading scales or mismatched axes |

## 6. Filters

- **Dimension filter:** Filters categorical values such as Region or Category.
- **Measure filter:** Filters aggregated numeric values, such as states with profit above a threshold.
- **Context filter:** Creates a primary filter that other filters evaluate within; useful for dependent filters and some performance cases.
- **Data source filter:** Applies to the entire data source and all connected views.
- **Extract filter:** Limits rows included in an extract, reducing extract size.
- **Quick filter:** The visible filter control users interact with on a worksheet or dashboard.
- **Relative filter:** Filters relative values such as the latest period, but requires an actual date or time field. The current dataset has no date field.

Dimension filters usually select categories, measure filters act after aggregation, context filters establish a filtering scope, and source or extract filters restrict data earlier in the pipeline.

## 7. Calculated Fields

Tableau calculations use field names in square brackets.

```tableau
SUM([Sales])
AVG([Discount])
COUNT([Sales])
COUNTD([State])

IF [Profit] < 0 THEN "Loss"
ELSE "Profit"
END

CASE [Category]
WHEN "Technology" THEN "Tech"
WHEN "Furniture" THEN "Furniture"
ELSE "Other"
END

IIF([Profit] < 0, "Loss", "Profit")

ZN([Profit])

IFNULL([Region], "Unknown")
```

### Profit Margin

```tableau
IF SUM([Sales]) = 0 THEN 0
ELSE SUM([Profit]) / SUM([Sales])
END
```

Format this result as a percentage. The calculation uses aggregated profit divided by aggregated sales, which is generally more appropriate for an overall margin than averaging row-level margins.

## 8. Table Calculations

- **Running Total:** Accumulates values across an ordered view. Useful for cumulative regional sales.
- **Difference:** Shows the change between the current and previous value.
- **Percent Difference:** Shows relative change between values.
- **Percent of Total:** Shows each category's contribution to total sales or profit.
- **Rank:** Orders categories, states, or sub-categories by a measure.
- **Moving Average:** Smooths short-term variation across an ordered sequence.

Table calculations depend on the view's addressing and partitioning. Always check **Compute Using** and confirm the order is meaningful. Moving averages and time-based differences require a valid ordered field; monthly analysis is not supported by the current dataset.

## 9. Parameters

A **parameter** is a user-controlled value that can be used in calculations, filters, reference lines, or sheet selection. A parameter is not automatically tied to a field, while a filter selects values directly from a field.

**Business example:** Create a parameter called `Selected Metric` with Sales, Profit, and Quantity options. A calculated field can return the selected measure, allowing one chart to switch between business metrics.

Parameters make dashboards interactive by letting users change thresholds, metrics, rankings, or display logic without editing the workbook.

## 10. Dashboard Design

1. Start with a clear business question and audience.
2. Place KPI cards at the top for Sales, Profit, Quantity, and Profit Margin.
3. Add a small, organized set of filters.
4. Use charts that match the analytical question.
5. Arrange views in a logical reading order: overview, comparisons, details, and actions.
6. Use meaningful titles, units, subtitles, and tooltips.
7. Apply consistent colors, number formats, fonts, and spacing.
8. Use color intentionally, such as one color for positive profit and another for losses.
9. Keep unnecessary decorations and chart types out of the report.
10. Test filtering, tooltips, navigation, and readability at the target screen size.

## 11. Retail Tableau Dashboard Design

### KPI cards

- `SUM(Sales)` — Total Sales
- `SUM(Profit)` — Total Profit
- `SUM(Quantity)` — Quantity Sold
- Profit Margin calculated as `SUM(Profit) / SUM(Sales)`

### Worksheets and charts

- **Sales by Category:** Column chart with Category and `SUM(Sales)`.
- **Profit by Category:** Bar chart with Category and `SUM(Profit)`, using different colors for positive and negative results.
- **Sales by Region:** Bar chart with Region and `SUM(Sales)`.
- **Profit by Region:** Bar chart with Region and `SUM(Profit)`.
- **Top States by Sales:** State bar chart sorted descending by `SUM(Sales)`, filtered to the top 10.
- **Bottom States by Profit:** State bar chart sorted ascending by `SUM(Profit)`, filtered to the bottom 10.
- **Segment Performance:** Table or bars comparing Segment, Sales, Profit, Quantity, Discount, and Profit Margin.
- **Discount vs Profit:** Scatter plot with Discount on Columns, Profit on Rows, and Category on Color.
- **Sub-Category Performance:** Table or ranked bar chart with Sub-Category, Sales, Profit, Discount, and Profit Margin.

### Recommended filters

Use `Segment`, `Category`, `Sub-Category`, `Region`, `State`, and `Ship Mode` as dashboard filters. Avoid adding unavailable customer or date fields.

## 12. Business Insights

- **Highest sales category:** Sort Category by `SUM(Sales)` descending.
- **Most profitable category:** Sort Category by `SUM(Profit)` descending.
- **Strongest region:** Compare regions by the selected measure; state whether the conclusion uses sales, profit, or margin.
- **Weakest region:** Sort by profit or margin ascending and investigate low or negative results.
- **Most profitable segment:** Compare Segment by `SUM(Profit)` and Profit Margin.
- **Loss-making sub-categories:** Filter or color sub-categories where `SUM(Profit) < 0`.
- **Discount-profit relationship:** Use a Discount versus Profit scatter plot and discount bands. Describe an observed relationship, not proven causation.

## 13. Tableau vs Power BI

| Area | Tableau | Power BI |
|---|---|---|
| Ease of use | Strong drag-and-drop visual exploration | Strong Microsoft-integrated workflow |
| Visualization | Highly flexible visual analysis | Broad visual library and custom visuals |
| Data modeling | Relationships and data sources | Semantic models, relationships, and DAX |
| Calculations | Tableau calculated fields and table calculations | DAX measures and calculated columns |
| Dashboard design | Flexible canvas and storytelling | Report pages, dashboards, and Microsoft ecosystem |
| Business intelligence | Strong visual discovery and sharing | Strong enterprise integration and governance |
| Learning curve | Intuitive visuals, advanced features take practice | Familiar to Microsoft users; DAX takes practice |
| Typical use cases | Exploratory analytics and visual storytelling | Enterprise reporting and governed BI |

## 14. Tableau vs Excel

Use **Excel** for quick calculations, manual review, compact datasets, formulas, and Pivot Tables. Use **Tableau** for interactive visual exploration, reusable dashboards, richer filtering, and sharing with multiple stakeholders. They can work together: Excel can provide a source file or validation workbook, while Tableau can turn prepared data into an interactive published dashboard.

## 15. Thirty Tableau Interview Questions

### Beginner

1. **What is Tableau?**  
   A visual analytics platform for connecting to data and creating interactive views.
2. **What is a worksheet?**  
   One visualization or view in a workbook.
3. **What is a dashboard?**  
   A layout containing multiple worksheets.
4. **What is a dimension?**  
   A descriptive field used to group data.
5. **What is a measure?**  
   A numeric field that can be aggregated.
6. **What is a mark?**  
   A visual representation of data, such as a bar or circle.
7. **What is a workbook?**  
   A Tableau file containing views and data connections.
8. **What is the difference between discrete and continuous?**  
   Discrete creates separate headers; continuous creates an axis or range.
9. **How do you connect a CSV?**  
   Use the Text File connector and select the CSV.
10. **What is a quick filter?**  
    A visible control for selecting field values.

### Intermediate

11. **Live connection or extract?**  
    Use live for source freshness and extract for speed, portability, or reduced source load.
12. **What is a calculated field?**  
    A reusable formula created from fields and functions.
13. **What is a context filter?**  
    A primary filter whose result defines the scope for other filters.
14. **What is a data source filter?**  
    A filter applied across views using the same data source.
15. **How do you create a top 10 list?**  
    Use a Top filter on the dimension based on a measure.
16. **What is a table calculation?**  
    A calculation performed across the results displayed in a view.
17. **How do you calculate profit margin?**  
    Use `SUM([Profit]) / SUM([Sales])`, protected for zero sales.
18. **Why use a scatter plot?**  
    To compare two numeric measures and inspect their relationship.
19. **What is a parameter?**  
    A user-controlled value that can change calculations or view behavior.
20. **How do you improve dashboard usability?**  
    Use clear layout, limited filters, consistent formatting, useful tooltips, and logical navigation.

### Advanced

21. **What is the difference between a dimension filter and measure filter?**  
    A dimension filter selects categories; a measure filter restricts aggregated numeric results.
22. **What is the order of operations?**  
    It is Tableau's sequence for applying extract, source, context, dimension, measure, and table-calculation filters.
23. **Why use an extract?**  
    Extracts can improve performance and support offline or portable analysis.
24. **What is a dual-axis chart?**  
    A chart with two measures using separate axes, often synchronized when appropriate.
25. **What is a dashboard action?**  
    An interaction such as filter, highlight, URL, parameter, or navigation behavior.
26. **What is a set?**  
    A custom subset of dimension members that can be used in analysis or calculations.
27. **How do you optimize a slow workbook?**  
    Reduce unnecessary marks, simplify calculations, limit filters, use extracts, and review performance recording.
28. **What is a level of detail expression?**  
    A calculation that controls the granularity at which a value is computed.
29. **How do you validate a Tableau dashboard?**  
    Reconcile totals with the source, test filters, inspect calculations, and verify edge cases.
30. **How do you avoid misleading visual analysis?**  
    Use honest scales, clear labels, appropriate chart types, and distinguish association from causation.

## 16. Scenario Questions

### 1. A manager wants the highest-profit category.

- **Business problem:** Identify the strongest category by profit.
- **Tableau approach:** Build a sorted Category bar chart using `SUM(Profit)`.
- **Visual/filter/calculation:** Bar chart, Category filter, profit measure.
- **Expected outcome:** A clear ranking with the top category visible.

### 2. A manager wants weak states.

- **Business problem:** Find geographic areas with low profitability.
- **Tableau approach:** Create a State bar chart sorted ascending by `SUM(Profit)`.
- **Visual/filter/calculation:** Bar chart, measure filter for negative profit if needed.
- **Expected outcome:** Bottom states prioritized for review.

### 3. The business wants to examine discount risk.

- **Business problem:** Understand whether high discount values appear with lower profit.
- **Tableau approach:** Use a Discount versus Profit scatter plot with Category on Color.
- **Visual/filter/calculation:** Scatter plot, tooltips, discount range calculated field.
- **Expected outcome:** An evidence-based view of the observed association.

### 4. Executives need a one-page overview.

- **Business problem:** Monitor key performance quickly.
- **Tableau approach:** Place KPI cards, category and region charts, and a short insight area on a dashboard.
- **Visual/filter/calculation:** Cards, bars, filters, Profit Margin calculation.
- **Expected outcome:** A concise management overview.

### 5. Users need to compare segments.

- **Business problem:** Understand Consumer, Corporate, and Home Office performance.
- **Tableau approach:** Build a Segment table and sales/profit charts with Segment as a filter.
- **Visual/filter/calculation:** Bars, table, sales mix, profit margin.
- **Expected outcome:** Clear segment contribution and profitability comparison.

### 6. A stakeholder wants exact sub-category values.

- **Business problem:** Review detailed product hierarchy performance.
- **Tableau approach:** Build a sorted table with Sub-Category, Sales, Profit, Discount, and Margin.
- **Visual/filter/calculation:** Table, conditional color, calculated margin.
- **Expected outcome:** Exact values and visible low-profit sub-categories.

### 7. A dashboard has too many filters.

- **Business problem:** Users are confused by a crowded interface.
- **Tableau approach:** Keep only decision-relevant filters, group them, and use dashboard actions where possible.
- **Visual/filter/calculation:** Quick filters, filter actions, organized layout.
- **Expected outcome:** Easier navigation and faster analysis.

### 8. A KPI shows an error when sales are zero.

- **Business problem:** Profit margin cannot divide by zero.
- **Tableau approach:** Use an `IF SUM([Sales]) = 0 THEN 0` guard.
- **Visual/filter/calculation:** Calculated field and KPI card.
- **Expected outcome:** A stable, documented KPI.

### 9. A report needs geographic context.

- **Business problem:** Compare state or city performance spatially.
- **Tableau approach:** Assign the correct geographic role and map `SUM(Profit)` or `SUM(Sales)`.
- **Visual/filter/calculation:** Map, color scale, geographic filter.
- **Expected outcome:** Geographic concentration and weak areas become easier to see.

### 10. A stakeholder asks for monthly trends.

- **Business problem:** Show changes over time.
- **Tableau approach:** First verify a valid date field exists. The current dataset has no date column, so do not create a monthly chart from invented data.
- **Visual/filter/calculation:** A line chart would be appropriate only with a genuine date field.
- **Expected outcome:** An honest limitation and a clear future data requirement.

## 17. Project Interview Answer

“I would convert my Retail Business Analysis project into Tableau by connecting Tableau Desktop to the supplied CSV and validating the available fields. I would prepare the numeric types for Sales, Quantity, Discount, and Profit, inspect missing values and duplicates, and create calculated fields for profit margin and profit status.

I would build KPI cards for total sales, total profit, quantity sold, and profit margin. Then I would create category, regional, state, segment, shipping, sub-category, and discount-versus-profit worksheets and combine them into dashboard pages. Filters for Segment, Category, Sub-Category, Region, State, and Ship Mode would update the views. Finally, I would add tooltips, rankings, conditional formatting, and concise insights, then validate totals against the Python dashboard. I would not add customer or time-series analysis because those fields are not available.”

## 18. Quick Revision Cheat Sheet

### Important terminology

- Workbook = collection of Tableau content.
- Worksheet = one view.
- Dashboard = multiple views on one screen.
- Story = sequence of views.
- Dimension = descriptive grouping field.
- Measure = numeric aggregated field.
- Mark = visual data point.
- Extract = optimized local copy.
- Parameter = user-controlled value.
- Context filter = primary filtering scope.

### Important calculations

```tableau
SUM([Sales])
AVG([Discount])
COUNT([Sales])
COUNTD([State])
IF [Profit] < 0 THEN "Loss" ELSE "Profit" END
ZN([Profit])
IFNULL([Region], "Unknown")
IF SUM([Sales]) = 0 THEN 0
ELSE SUM([Profit]) / SUM([Sales])
END
```

### Chart selection

- Bars/columns = category comparison and ranking.
- Line/area = ordered trends; use a real date for time analysis.
- Donut = simple composition.
- Scatter = two numeric measures.
- Heat map = two-dimensional intensity.
- Map = geographic patterns.
- Table = exact detail.
- Dual axis = two measures with careful scale control.

### Filter types

- Dimension, measure, context, source, extract, quick, and relative filters.
- Relative filters require a date or time field.

### Dashboard best practices

- Lead with KPIs.
- Keep filters focused.
- Sort rankings logically.
- Use consistent number formats and colors.
- Explain calculations in tooltips or subtitles.
- Test empty results and zero denominators.
- Validate totals against the source.
- Do not claim unsupported fields or causal conclusions.

**TABLEAU INTERVIEW MODULE: COMPLETE**
