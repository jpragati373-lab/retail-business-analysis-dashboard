# Excel Interview Preparation — Retail Data Analyst

This module uses the project's actual fields:

`Ship Mode`, `Segment`, `Country`, `City`, `State`, `Postal Code`, `Region`, `Category`, `Sub-Category`, `Sales`, `Quantity`, `Discount`, and `Profit`.

It does not assume Order Date, Order ID, Customer ID, Customer Name, or Product Name.

## 1. Excel Fundamentals

- **Workbook:** An Excel file containing one or more worksheets.
- **Worksheet:** One spreadsheet tab made of rows and columns.
- **Row:** A horizontal set of cells, identified by numbers.
- **Column:** A vertical set of cells, identified by letters.
- **Cell:** The intersection of a row and column, such as `A1`.
- **Range:** A selected group of cells, such as `A1:D10`.
- **Table:** A structured range with headers, filters, automatic expansion, and structured references.
- **Sorting:** Reordering rows by one or more columns.
- **Filtering:** Showing only rows that meet selected conditions.
- **Freeze Panes:** Keeping headers or selected rows and columns visible while scrolling.

For analysis, convert the retail data to an Excel Table named `RetailData`. Structured references such as `RetailData[Sales]` are easier to maintain than fixed cell ranges.

## 2. Important Excel Functions

Assume the data is in an Excel Table named `RetailData`.

| Function | Syntax | Retail example |
|---|---|---|
| `SUM` | `=SUM(range)` | `=SUM(RetailData[Sales])` |
| `AVERAGE` | `=AVERAGE(range)` | `=AVERAGE(RetailData[Discount])` |
| `COUNT` | `=COUNT(range)` | `=COUNT(RetailData[Sales])` |
| `COUNTA` | `=COUNTA(range)` | `=COUNTA(RetailData[State])` |
| `COUNTIF` | `=COUNTIF(range, criteria)` | `=COUNTIF(RetailData[Region],"West")` |
| `COUNTIFS` | `=COUNTIFS(range1,criteria1,...)` | `=COUNTIFS(RetailData[Region],"West",RetailData[Profit],">0")` |
| `SUMIF` | `=SUMIF(criteria_range, criteria, sum_range)` | `=SUMIF(RetailData[Category],"Technology",RetailData[Sales])` |
| `SUMIFS` | `=SUMIFS(sum_range, range1, criteria1,...)` | `=SUMIFS(RetailData[Profit],RetailData[Region],"West",RetailData[Discount],">0.2")` |
| `AVERAGEIF` | `=AVERAGEIF(range, criteria, average_range)` | `=AVERAGEIF(RetailData[Category],"Furniture",RetailData[Discount])` |
| `AVERAGEIFS` | `=AVERAGEIFS(average_range, range1, criteria1,...)` | `=AVERAGEIFS(RetailData[Profit],RetailData[Region],"East",RetailData[Profit],">0")` |
| `IF` | `=IF(test, value_if_true, value_if_false)` | `=IF([@Profit]<0,"Loss","Profit")` |
| `AND` | `=AND(test1,test2)` | `=AND([@Discount]>0.2,[@Profit]<0)` |
| `OR` | `=OR(test1,test2)` | `=OR([@Region]="West",[@Region]="East")` |
| `IFERROR` | `=IFERROR(value, fallback)` | `=IFERROR([@Profit]/[@Sales],0)` |
| `ROUND` | `=ROUND(number, digits)` | `=ROUND([@Sales],2)` |
| `MIN` | `=MIN(range)` | `=MIN(RetailData[Profit])` |
| `MAX` | `=MAX(range)` | `=MAX(RetailData[Profit])` |

For a standard range instead of a Table, replace structured references with ranges such as `$J$2:$J$10000`.

## 3. Lookup Functions

Assume a separate generic lookup table has a key in column A and a result in column B.

### VLOOKUP

```excel
=VLOOKUP(A2,LookupTable!$A$2:$B$100,2,FALSE)
```

Searches the first column and returns a value from a column to its right. `FALSE` requests an exact match.

### HLOOKUP

```excel
=HLOOKUP(B1,LookupTable!$B$1:$G$3,3,FALSE)
```

Searches the first row and returns a value from a row below it. It is useful for horizontal layouts but less common in well-designed models.

### XLOOKUP

```excel
=XLOOKUP(A2,LookupTable[Key],LookupTable[Description],"Not found")
```

Searches one range and returns the corresponding value from another range. It supports exact matching by default, lookup in either direction, and a not-found result.

### INDEX

```excel
=INDEX(LookupTable[Description],5)
```

Returns the value at a specified position in a range.

### MATCH

```excel
=MATCH(A2,LookupTable[Key],0)
```

Returns the position of a value in a range. `0` requests an exact match.

### XLOOKUP vs VLOOKUP

XLOOKUP is generally more flexible: it can look left or right, defaults to exact matching, and accepts a not-found message. VLOOKUP requires the lookup column to be first and uses a column number, so inserting columns can make formulas fragile.

### INDEX/MATCH vs XLOOKUP

INDEX/MATCH works in older Excel versions and separates position-finding from value-returning. XLOOKUP is easier to read and usually requires less formula complexity when it is available.

The current retail dataset is self-contained, so these lookups are generic concepts rather than required dashboard operations.

## 4. Text Functions

Assume `A2` contains text.

```excel
=LEFT(A2,3)
=RIGHT(A2,3)
=MID(A2,2,5)
=LEN(A2)
=TRIM(A2)
=UPPER(A2)
=LOWER(A2)
=PROPER(A2)
=CONCAT(A2," - ",B2)
=TEXTJOIN(", ",TRUE,A2:C2)
=FIND("-",A2)
=SUBSTITUTE(A2,"old","new")
```

These return the first characters, last characters, a substring, character count, trimmed text, uppercase text, lowercase text, title case, combined text, delimiter-joined text, delimiter position, and replaced text respectively.

Use `TRIM`, `UPPER`, `LOWER`, and `SUBSTITUTE` to standardize inconsistent labels such as regions or ship modes before analysis.

## 5. Date Functions

```excel
=TODAY()
=NOW()
=YEAR(A2)
=MONTH(A2)
=DAY(A2)
=DATE(2026,9,3)
=DATEDIF(A2,B2,"d")
```

These return today's date, the current date and time, date parts, a constructed date, and the difference between two dates respectively.

Date analysis requires an actual date column. The current retail dataset has no date field, so these functions are not applicable to its existing analysis. A future dataset with a validated date column could support monthly or year-over-year analysis.

## 6. Data Cleaning in Excel

- **Remove duplicates:** Select the data and use **Data → Remove Duplicates** after confirming which columns define a duplicate.
- **Handle blanks:** Filter blanks, determine whether they mean missing, not applicable, or unknown, then replace or preserve them consistently.
- **Fix inconsistent text:** Use Find and Replace, `TRIM`, `CLEAN`, and standardized labels.
- **Remove extra spaces:** Use `=TRIM(A2)`. For non-printing characters, use `=CLEAN(A2)`.
- **Standardize values:** Use controlled lists, consistent capitalization, and validation rules.
- **Detect errors:** Filter `#N/A`, `#VALUE!`, `#DIV/0!`, and other formula errors; investigate the source.
- **Validate data:** Check row counts, expected columns, numeric ranges, totals, and unexpected categories.
- **Convert data types:** Set sales and profit to numbers, quantity to whole numbers, discount to a numeric percentage, and text fields to text.

For this project, validate `Sales`, `Quantity`, `Discount`, and `Profit` before creating KPI calculations or Pivot Tables.

## 7. Pivot Tables

### Creating a Pivot Table

1. Select a cell in the `RetailData` table.
2. Choose **Insert → PivotTable**.
3. Select a new or existing worksheet.
4. Drag fields into Rows, Columns, Values, and Filters.
5. Format numbers and sort the results.
6. Refresh after the source data changes.

### Pivot Areas

- **Rows:** The grouping dimension, such as `Category` or `Region`.
- **Columns:** A second dimension for side-by-side comparison, such as `Segment`.
- **Values:** Measures such as Sum of `Sales`, Sum of `Profit`, or Average of `Discount`.
- **Filters:** Report-level selections such as `Ship Mode` or `State`.

### Retail examples

- Rows: `Category`; Values: Sum of `Sales` and Sum of `Profit`.
- Rows: `Region`; Values: Sum of `Profit`; sort largest to smallest.
- Rows: `Segment`; Columns: `Category`; Values: Sum of `Sales`.
- Rows: `Sub-Category`; Values: Average of `Discount` and Sum of `Profit`.

### Grouping, sorting, and calculated fields

Pivot Tables can group values where appropriate, sort by a measure, and use calculated fields for simple derived metrics. For profit margin, a formula such as `Profit/Sales` must be interpreted carefully; an aggregated margin using total profit divided by total sales is usually more meaningful than averaging row-level margins.

## 8. Excel Charts

- **Column Chart:** Use for comparing a small number of categories, such as sales by category. Avoid long labels and too many columns.
- **Bar Chart:** Use for ranked states, cities, or sub-categories with long names. Do not leave the bars unsorted.
- **Line Chart:** Use for ordered time or sequence data. The current dataset has no date column, so a monthly line chart is not supported.
- **Pie/Donut Chart:** Use for a simple part-to-whole view with only a few segments. Do not use it for many similar values.
- **Scatter Plot:** Use to compare two numeric variables, such as Discount and Profit. Do not claim causation from the pattern alone.
- **Combo Chart:** Use when comparing measures with different scales, such as sales columns and profit-margin line. Avoid confusing secondary axes.

Common mistakes include cluttered labels, poor sorting, excessive colors, misleading axes, 3-D effects, too many categories, and charts without a clear title or unit.

## 9. Conditional Formatting

- **Highlight rules:** Color values greater than, less than, equal to, or containing a condition.
- **Data bars:** Show relative magnitude inside cells.
- **Color scales:** Use gradients to show low-to-high values.
- **Duplicate values:** Highlight repeated records or labels for investigation.
- **Top/Bottom rules:** Highlight the top or bottom percentage or number of values.

Examples:

- Highlight negative `Profit` in red.
- Add data bars to `Sales`.
- Apply a color scale to `Profit Margin`.
- Highlight duplicate combinations after confirming the business definition of a duplicate.
- Use Top 10 rules for high-profit states.

## 10. Retail Analysis in Excel

The following questions use only the available fields.

### 1. What are total sales by category?

**Pivot Table:** Rows = `Category`; Values = Sum of `Sales`; sort descending.

**Formula example:**

```excel
=SUMIF(RetailData[Category],A2,RetailData[Sales])
```

### 2. What is total profit by region?

**Pivot Table:** Rows = `Region`; Values = Sum of `Profit`; sort descending.

```excel
=SUMIF(RetailData[Region],A2,RetailData[Profit])
```

### 3. Which states rank highest by sales?

**Pivot Table:** Rows = `State`; Values = Sum of `Sales`; sort largest to smallest and keep the top 10.

### 4. Which states have the lowest profit?

**Pivot Table:** Rows = `State`; Values = Sum of `Profit`; sort smallest to largest.

### 5. What is profit by segment?

**Pivot Table:** Rows = `Segment`; Values = Sum of `Profit`.

```excel
=SUMIF(RetailData[Segment],A2,RetailData[Profit])
```

### 6. What is the average discount by category?

**Pivot Table:** Rows = `Category`; Values = Average of `Discount`.

```excel
=AVERAGEIF(RetailData[Category],A2,RetailData[Discount])
```

### 7. What quantity is sold by sub-category?

**Pivot Table:** Rows = `Sub-Category`; Values = Sum of `Quantity`.

### 8. What is profit margin by region?

Create Pivot values for Sum of `Profit` and Sum of `Sales`, then calculate beside the Pivot:

```excel
=IFERROR(B2/C2,0)
```

Format the result as a percentage.

### 9. Which records are loss-making?

Add a Table calculated column:

```excel
=IF([@Profit]<0,"Loss-making","Profitable")
```

Filter the result to `Loss-making`.

### 10. Which categories have high discounts and negative profit?

Use a helper column:

```excel
=IF(AND([@Discount]>0.2,[@Profit]<0),"Review","")
```

Filter to `Review`, or use a Pivot Table with Category and Sum of Profit.

### 11. What is sales by shipping mode?

**Pivot Table:** Rows = `Ship Mode`; Values = Sum of `Sales`.

### 12. Which cities generate the most profit?

**Pivot Table:** Rows = `City`; Values = Sum of `Profit`; sort descending.

### 13. What is the sales mix by segment?

**Pivot Table:** Rows = `Segment`; Values = Sum of `Sales`.

Show values as **% of Grand Total**, then create a donut chart.

### 14. Which category and sub-category combinations perform best?

**Pivot Table:** Rows = `Category`, then `Sub-Category`; Values = Sum of `Sales` and Sum of `Profit`; sort by profit.

### 15. Which discount ranges have the strongest profitability?

Create a helper column:

```excel
=IF([@Discount]=0,"0%",
 IF([@Discount]<=0.1,"1-10%",
 IF([@Discount]<=0.2,"11-20%",
 IF([@Discount]<=0.3,"21-30%","31%+"))))
```

Create a Pivot Table with Rows = `Discount Range`, Values = Sum of `Sales`, Sum of `Profit`, Sum of `Quantity`, and Count of records. Calculate margin as total profit divided by total sales.

## 11. Data Analyst Excel Interview Questions

### Beginner

1. **What is the difference between a workbook and worksheet?**  
   A workbook is the Excel file; a worksheet is one tab inside it.
2. **What is a cell range?**  
   A group of cells, such as `A1:D10`.
3. **Why use an Excel Table?**  
   It provides structured references, automatic filters, and expanding formulas.
4. **What is sorting?**  
   Reordering records based on one or more columns.
5. **What is filtering?**  
   Displaying only records that meet selected criteria.
6. **What does `SUM` do?**  
   Adds numeric values.
7. **What is the difference between `COUNT` and `COUNTA`?**  
   `COUNT` counts numeric cells; `COUNTA` counts non-empty cells.
8. **What does `IF` do?**  
   Returns one result when a condition is true and another when it is false.
9. **Why freeze panes?**  
   To keep headers visible while scrolling.
10. **What is a Pivot Table?**  
    A tool for quickly summarizing and grouping data.

### Intermediate

11. **When would you use `SUMIFS`?**  
    When adding values that meet multiple conditions.
12. **How do you find duplicates?**  
    Use Conditional Formatting or Remove Duplicates after defining the duplicate key.
13. **How do you handle blanks?**  
    Profile them first, then replace, remove, or preserve them according to their meaning.
14. **Why use `IFERROR`?**  
    To display a controlled result instead of a formula error.
15. **What is the difference between `VLOOKUP` and `XLOOKUP`?**  
    XLOOKUP is more flexible, supports left lookups, exact matching by default, and custom not-found results.
16. **What does `COUNTIFS` do?**  
    Counts rows meeting multiple conditions.
17. **How do you calculate a percentage safely?**  
    Divide by the denominator and use `IFERROR` or an explicit zero check.
18. **How do you sort a Pivot Table by profit?**  
    Right-click a profit value and choose the desired sort order.
19. **What is conditional formatting useful for?**  
    Quickly identifying high, low, negative, duplicate, or unusual values.
20. **How do you make a chart responsive to filters?**  
    Base it on an Excel Table or Pivot Table and use slicers or filters.

### Advanced

21. **What is the difference between a formula and a calculated field?**  
    A formula works in cells; a Pivot calculated field applies a formula within a Pivot Table model.
22. **Why can averaging row-level profit margins be misleading?**  
    Small and large transactions receive equal weight. Total profit divided by total sales is often a better overall margin.
23. **How would you validate an analysis workbook?**  
    Reconcile totals, check row counts, inspect formulas, test filters, and compare selected results with the source.
24. **What is Power Query in Excel?**  
    A repeatable tool for importing and transforming data.
25. **How can you improve workbook performance?**  
    Use Tables, avoid excessive volatile formulas, reduce unnecessary formatting, and summarize large data with Pivot Tables or Power Query.
26. **How do you create a top 3 per category analysis?**  
    Use a Pivot Table with sorting and filters, or rank rows with formulas and filter rank values.
27. **How do you identify a running total?**  
    Use a cumulative formula such as `=SUM($B$2:B2)` or a Pivot Table running-total setting.
28. **How do you handle an unavailable date field?**  
    State that date analysis cannot be performed and avoid inventing a date dimension.
29. **When would you use a helper column?**  
    When a reusable row-level classification, such as a discount range or profit status, simplifies analysis.
30. **How do you protect business users from formula errors?**  
    Use validation, clear labels, safe formulas, protected cells, and instructions for refresh and interpretation.

## 12. Scenario Questions

### 1. A manager wants total sales by category.

- **Problem:** Compare category revenue.
- **Approach:** Create a Pivot Table with Category in Rows and Sales in Values.
- **Feature/function:** Pivot Table and `SUM`.
- **Expected result:** A sorted category sales summary.

### 2. A manager wants to find weak states.

- **Problem:** Identify geographic areas with low profit.
- **Approach:** Group State by Sum of Profit and sort ascending.
- **Feature/function:** Pivot Table, sorting, conditional formatting.
- **Expected result:** Bottom-profit states highlighted for review.

### 3. A manager asks whether high discounts are risky.

- **Problem:** Compare discount levels and profitability.
- **Approach:** Create discount-range and profit-status helper columns, then summarize profit by range.
- **Feature/function:** `IF`, `AND`, Pivot Table, scatter chart.
- **Expected result:** A clear comparison of profit across discount bands.

### 4. The source file contains extra spaces in regions.

- **Problem:** Filters split identical regions into separate labels.
- **Approach:** Create a cleaned helper field with `TRIM`, review values, and use the standardized field.
- **Feature/function:** `TRIM`, Find and Replace, data validation.
- **Expected result:** Consistent region grouping.

### 5. A report contains duplicate rows.

- **Problem:** Totals may be overstated.
- **Approach:** Profile duplicates, confirm the correct business key, and remove only confirmed duplicates.
- **Feature/function:** Remove Duplicates, Conditional Formatting.
- **Expected result:** Accurate and documented row-level data.

### 6. A KPI shows `#DIV/0!`.

- **Problem:** Profit margin has zero sales.
- **Approach:** Wrap the calculation with `IFERROR` or test the denominator.
- **Feature/function:** `IFERROR`, `IF`.
- **Expected result:** A safe result such as zero or `N/A`, according to the reporting rule.

### 7. A stakeholder wants the top 10 cities by profit.

- **Problem:** Rank many cities quickly.
- **Approach:** Create a City-profit Pivot Table, sort descending, and apply a Top 10 value filter.
- **Feature/function:** Pivot Table value filter and sorting.
- **Expected result:** A concise top-city ranking.

### 8. A user needs to explore one segment.

- **Problem:** Review selected segment performance.
- **Approach:** Add a Segment slicer connected to Pivot Tables and charts.
- **Feature/function:** Slicer and Pivot Table.
- **Expected result:** All linked visuals update for the chosen segment.

### 9. A recruiter asks for an exportable summary.

- **Problem:** Share analyzed results.
- **Approach:** Keep a clean summary worksheet with labeled KPI and Pivot Table outputs.
- **Feature/function:** Tables, Pivot Tables, Save/Export.
- **Expected result:** A reproducible workbook or CSV-style summary.

### 10. A stakeholder requests monthly trends.

- **Problem:** Analyze performance over time.
- **Approach:** First verify that a valid date column exists. If it does not, explain that monthly analysis is not supported by the current dataset.
- **Feature/function:** Date validation and transparent scope management.
- **Expected result:** No invented dates; a clear limitation and future requirement.

## 13. Excel vs Power BI

### Use Excel when:

- The dataset is small or moderate.
- The analysis is ad hoc or needs manual review.
- Users need formulas, quick calculations, or editable worksheets.
- A simple Pivot Table or one-off report is sufficient.

### Use Power BI when:

- The dashboard needs interactive sharing across many users.
- Data sources are larger or regularly refreshed.
- A governed data model and reusable measures are important.
- Users need centralized reports, drill-through, and cross-filtering.

### How they work together

Excel can prepare or validate data, while Power BI can publish an interactive semantic model and dashboard. Power BI can also connect to Excel workbooks, and Excel can connect to Power BI semantic models for Pivot-based analysis.

## 14. Quick Revision Cheat Sheet

### Important formulas

```excel
=SUM(range)
=AVERAGE(range)
=COUNT(range)
=COUNTIF(range,criteria)
=COUNTIFS(range1,criteria1,range2,criteria2)
=SUMIFS(sum_range,range1,criteria1)
=AVERAGEIFS(avg_range,range1,criteria1)
=IF(condition,true_value,false_value)
=IFERROR(value,fallback)
=ROUND(number,2)
=MIN(range)
=MAX(range)
```

### Lookup functions

- `XLOOKUP`: Preferred modern lookup when available.
- `VLOOKUP`: Exact match with `FALSE`; lookup column must be first.
- `INDEX/MATCH`: Flexible legacy combination.
- `HLOOKUP`: Lookup across a horizontal first row.

### Pivot Table concepts

- Rows = grouping dimension.
- Columns = second comparison dimension.
- Values = Sum, Average, Count, Min, or Max.
- Filters/Slicers = user selections.
- Sort = rank results by a measure.
- Refresh = update the summary after source changes.

### Data-cleaning tools

- Excel Tables
- Remove Duplicates
- Filters
- Find and Replace
- `TRIM` and `CLEAN`
- Data Validation
- Conditional Formatting
- Power Query

### Chart selection

- Column/bar = category comparison or ranking.
- Line = ordered time series only when a date exists.
- Donut = simple composition with few groups.
- Scatter = relationship between two numeric variables.
- Combo = measures with different scales.

### Interview tips

- Explain the business question before the formula.
- Use Tables and Pivot Tables for repeatable analysis.
- Validate totals and row counts.
- Protect ratios with `IFERROR`.
- Distinguish row-level calculations from aggregated KPIs.
- Be honest when a requested field is unavailable.
- Avoid claiming causation from a chart showing association.
- Keep workbooks labeled, sorted, documented, and easy to refresh.

**EXCEL INTERVIEW MODULE: COMPLETE**
