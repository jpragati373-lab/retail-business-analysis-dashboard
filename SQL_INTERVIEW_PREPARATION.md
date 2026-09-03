# SQL Interview Preparation — Retail Data Analyst

Assume the project table is named `retail_data` and contains:

`Ship Mode`, `Segment`, `Country`, `City`, `State`, `Postal Code`, `Region`, `Category`, `Sub-Category`, `Sales`, `Quantity`, `Discount`, `Profit`

Column names containing spaces should be quoted according to the SQL database, for example `"Ship Mode"` or `[Ship Mode]`.

## 1. SQL Fundamentals

- **Database:** An organized collection of related data.
- **Table:** A structured set of rows and columns, such as `retail_data`.
- **Row:** One record, such as one retail transaction.
- **Column:** One attribute, such as `Sales` or `Region`.
- **Primary Key:** A column or combination that uniquely identifies each row. Example: `transaction_id` in a generic sales table. This dataset has no declared unique ID.
- **Foreign Key:** A column that references a primary key in another table, such as `product_id`.
- **NULL:** A missing or unknown value. `NULL` is not the same as zero or an empty string.
- **Data Types:** Types define stored values, such as `INTEGER`, `DECIMAL`, `VARCHAR`, `DATE`, and `BOOLEAN`.

## 2. Basic SQL

```sql
SELECT Category, Sales
FROM retail_data;

SELECT DISTINCT Region
FROM retail_data;

SELECT *
FROM retail_data
WHERE Profit > 0
  AND Discount <= 0.20;

SELECT *
FROM retail_data
WHERE Category = 'Technology'
   OR Region = 'West';

SELECT *
FROM retail_data
WHERE NOT Segment = 'Consumer';

SELECT *
FROM retail_data
WHERE Region IN ('West', 'East');

SELECT *
FROM retail_data
WHERE Sales BETWEEN 100 AND 500;

SELECT *
FROM retail_data
WHERE City LIKE 'San%';

SELECT *
FROM retail_data
WHERE Profit IS NULL;

SELECT *
FROM retail_data
ORDER BY Sales DESC
LIMIT 10;
```

`WHERE` filters rows before aggregation. `AND` requires all conditions, `OR` requires at least one, and `NOT` reverses a condition.

## 3. Aggregation

```sql
SELECT COUNT(*) AS record_count,
       SUM(Sales) AS total_sales,
       SUM(Profit) AS total_profit,
       AVG(Discount) AS average_discount,
       MIN(Profit) AS minimum_profit,
       MAX(Profit) AS maximum_profit
FROM retail_data;

SELECT Category,
       SUM(Sales) AS total_sales,
       SUM(Profit) AS total_profit
FROM retail_data
GROUP BY Category
HAVING SUM(Profit) > 0
ORDER BY total_profit DESC;
```

- `COUNT()` counts rows or non-NULL values.
- `SUM()` adds numeric values.
- `AVG()` calculates the arithmetic mean.
- `MIN()` and `MAX()` find boundary values.
- `GROUP BY` creates one result group per dimension.
- `HAVING` filters grouped results after aggregation.

## 4. Joins

Assume generic tables `orders`, `products`, and `employees`.

```sql
-- Matching rows only
SELECT o.order_id, p.product_name
FROM orders o
INNER JOIN products p ON o.product_id = p.product_id;

-- Keep every order, even without a matching product
SELECT o.order_id, p.product_name
FROM orders o
LEFT JOIN products p ON o.product_id = p.product_id;

-- Keep every product, even without an order
SELECT o.order_id, p.product_name
FROM orders o
RIGHT JOIN products p ON o.product_id = p.product_id;

-- Keep unmatched rows from both tables
SELECT o.order_id, p.product_name
FROM orders o
FULL OUTER JOIN products p ON o.product_id = p.product_id;

-- Compare employees with their managers in the same table
SELECT e.employee_name, m.employee_name AS manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;
```

- **INNER JOIN:** Use when only matching records matter.
- **LEFT JOIN:** Use when all records from the primary table must remain.
- **RIGHT JOIN:** The reverse of a left join; less commonly used because tables can be reordered.
- **FULL OUTER JOIN:** Use when unmatched records from both sides are important.
- **SELF JOIN:** Join a table to itself for hierarchies or comparisons.

## 5. Subqueries

```sql
-- Scalar subquery: one value
SELECT *
FROM retail_data
WHERE Sales > (SELECT AVG(Sales) FROM retail_data);

-- Subquery in WHERE
SELECT *
FROM retail_data
WHERE Profit = (SELECT MAX(Profit) FROM retail_data);

-- IN subquery
SELECT *
FROM retail_data
WHERE State IN (
    SELECT State
    FROM retail_data
    GROUP BY State
    HAVING SUM(Profit) < 0
);

-- Correlated subquery: evaluated for each outer row
SELECT r.*
FROM retail_data r
WHERE Profit > (
    SELECT AVG(r2.Profit)
    FROM retail_data r2
    WHERE r2.Category = r.Category
);
```

## 6. CASE Statement

```sql
SELECT Category,
       Profit,
       CASE
           WHEN Profit < 0 THEN 'Loss'
           WHEN Profit = 0 THEN 'Break-even'
           ELSE 'Profit'
       END AS profit_status
FROM retail_data;

SELECT Discount,
       CASE
           WHEN Discount = 0 THEN '0%'
           WHEN Discount <= 0.10 THEN '1-10%'
           WHEN Discount <= 0.20 THEN '11-20%'
           WHEN Discount <= 0.30 THEN '21-30%'
           ELSE '31%+'
       END AS discount_range
FROM retail_data;
```

`CASE WHEN` converts business rules into categories or flags.

## 7. Window Functions

```sql
SELECT State, Profit,
       ROW_NUMBER() OVER (ORDER BY Profit DESC) AS row_num,
       RANK() OVER (ORDER BY Profit DESC) AS profit_rank,
       DENSE_RANK() OVER (ORDER BY Profit DESC) AS dense_rank
FROM (
    SELECT State, SUM(Profit) AS Profit
    FROM retail_data
    GROUP BY State
) s;

SELECT Region, Sales,
       SUM(Sales) OVER (ORDER BY Region) AS running_sales,
       AVG(Sales) OVER (PARTITION BY Region) AS regional_average
FROM retail_data;
```

- `ROW_NUMBER()` gives every row a unique sequence.
- `RANK()` gives ties the same rank and leaves gaps.
- `DENSE_RANK()` gives ties the same rank without gaps.
- `SUM() OVER()` and `AVG() OVER()` calculate across related rows without collapsing them.
- `PARTITION BY` defines independent groups.
- `ORDER BY` inside `OVER()` defines sequence or ranking order.

## 8. Common Data Analyst Queries

The first examples are **generic SQL examples** when the requested field is unavailable in this retail dataset.

### Top 10 products by sales — Generic example

```sql
SELECT ProductName, SUM(Sales) AS total_sales
FROM sales
GROUP BY ProductName
ORDER BY total_sales DESC
LIMIT 10;
```

### Highest- and lowest-profit category

```sql
SELECT Category, SUM(Profit) AS total_profit
FROM retail_data
GROUP BY Category
ORDER BY total_profit DESC
LIMIT 1;
```

Reverse the order for the lowest-profit category.

### Regional sales

```sql
SELECT Region, SUM(Sales) AS total_sales
FROM retail_data
GROUP BY Region
ORDER BY total_sales DESC;
```

### Average sales and total profit

```sql
SELECT AVG(Sales) AS average_sales,
       SUM(Profit) AS total_profit
FROM retail_data;
```

### Profit margin

```sql
SELECT 100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0) AS profit_margin
FROM retail_data;
```

### Duplicate records

```sql
SELECT "Ship Mode", Segment, City, State, Sales, Quantity, Discount, Profit,
       COUNT(*) AS duplicate_count
FROM retail_data
GROUP BY "Ship Mode", Segment, City, State, Sales, Quantity, Discount, Profit
HAVING COUNT(*) > 1;
```

### NULL values

```sql
SELECT COUNT(*) - COUNT(Profit) AS missing_profit,
       COUNT(*) - COUNT(Category) AS missing_category
FROM retail_data;
```

### Second-highest value

```sql
SELECT MAX(total_profit) AS second_highest_profit
FROM (
    SELECT SUM(Profit) AS total_profit
    FROM retail_data
    GROUP BY State
) x
WHERE total_profit < (
    SELECT MAX(total_profit)
    FROM (
        SELECT SUM(Profit) AS total_profit
        FROM retail_data
        GROUP BY State
    ) y
);
```

### Top 3 values per category

```sql
WITH subcategory_profit AS (
    SELECT Category, "Sub-Category",
           SUM(Profit) AS total_profit
    FROM retail_data
    GROUP BY Category, "Sub-Category"
),
ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY Category ORDER BY total_profit DESC
           ) AS rn
    FROM subcategory_profit
)
SELECT *
FROM ranked
WHERE rn <= 3;
```

### Running total

```sql
SELECT Region, Sales,
       SUM(Sales) OVER (ORDER BY Region) AS running_total
FROM (
    SELECT Region, SUM(Sales) AS Sales
    FROM retail_data
    GROUP BY Region
) x;
```

### Ranking

```sql
SELECT State, total_profit,
       RANK() OVER (ORDER BY total_profit DESC) AS profit_rank
FROM (
    SELECT State, SUM(Profit) AS total_profit
    FROM retail_data
    GROUP BY State
) x;
```

### Month-over-month analysis — Generic example

This requires a date column, which is not available in the retail dataset.

```sql
WITH monthly_sales AS (
    SELECT DATE_TRUNC('month', order_date) AS month,
           SUM(sales) AS total_sales
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT month, total_sales,
       LAG(total_sales) OVER (ORDER BY month) AS previous_month_sales,
       total_sales - LAG(total_sales) OVER (ORDER BY month) AS change
FROM monthly_sales;
```

## 9. Retail Business SQL Practice

Each exercise uses only the available retail fields.

### 1. Total sales by category

**Problem:** Calculate sales for each category.  
**SQL:**

```sql
SELECT Category, SUM(Sales) AS total_sales
FROM retail_data
GROUP BY Category
ORDER BY total_sales DESC;
```

**Expected logic:** Group by category and sum sales.  
**Explanation:** Shows which categories contribute most revenue.

### 2. Most profitable category

**Problem:** Find the category with the highest total profit.  
**SQL:**

```sql
SELECT Category, SUM(Profit) AS total_profit
FROM retail_data
GROUP BY Category
ORDER BY total_profit DESC
LIMIT 1;
```

**Expected logic:** Aggregate profit, sort descending, keep one row.  
**Explanation:** Identifies the strongest category by absolute profit.

### 3. Loss-making sub-categories

**Problem:** Find sub-categories with negative total profit.  
**SQL:**

```sql
SELECT "Sub-Category", SUM(Profit) AS total_profit
FROM retail_data
GROUP BY "Sub-Category"
HAVING SUM(Profit) < 0
ORDER BY total_profit;
```

**Expected logic:** Filter grouped profit with `HAVING`.  
**Explanation:** Finds sub-categories requiring attention.

### 4. Regional profitability

**Problem:** Calculate sales, profit, and margin by region.  
**SQL:**

```sql
SELECT Region,
       SUM(Sales) AS sales,
       SUM(Profit) AS profit,
       100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0) AS profit_margin
FROM retail_data
GROUP BY Region
ORDER BY profit DESC;
```

**Expected logic:** Aggregate first, then calculate margin safely.  
**Explanation:** Compares regional scale and efficiency.

### 5. Top 10 states by sales

**Problem:** Rank states by total sales.  
**SQL:**

```sql
SELECT State, SUM(Sales) AS total_sales
FROM retail_data
GROUP BY State
ORDER BY total_sales DESC
LIMIT 10;
```

**Expected logic:** Group, sum, sort, limit.  
**Explanation:** Identifies the largest state markets.

### 6. Bottom 10 cities by profit

**Problem:** Find the ten lowest-profit cities.  
**SQL:**

```sql
SELECT City, SUM(Profit) AS total_profit
FROM retail_data
GROUP BY City
ORDER BY total_profit
LIMIT 10;
```

**Expected logic:** Sort aggregated profit ascending.  
**Explanation:** Highlights weak geographic locations.

### 7. Quantity by segment

**Problem:** Calculate quantity sold by segment.  
**SQL:**

```sql
SELECT Segment, SUM(Quantity) AS quantity_sold
FROM retail_data
GROUP BY Segment
ORDER BY quantity_sold DESC;
```

**Expected logic:** Group segment and sum quantity.  
**Explanation:** Compares volume contribution.

### 8. Average discount by category

**Problem:** Find average discount per category.  
**SQL:**

```sql
SELECT Category, AVG(Discount) AS average_discount
FROM retail_data
GROUP BY Category
ORDER BY average_discount DESC;
```

**Expected logic:** Use `AVG()` by category.  
**Explanation:** Shows where discounting is most common.

### 9. High-discount loss records

**Problem:** Find records with discount above 20% and negative profit.  
**SQL:**

```sql
SELECT *
FROM retail_data
WHERE Discount > 0.20
  AND Profit < 0;
```

**Expected logic:** Apply two row-level conditions.  
**Explanation:** Supports review of potentially risky transactions.

### 10. Sales by shipping mode

**Problem:** Compare sales across shipping modes.  
**SQL:**

```sql
SELECT "Ship Mode", SUM(Sales) AS total_sales
FROM retail_data
GROUP BY "Ship Mode"
ORDER BY total_sales DESC;
```

**Expected logic:** Group by shipping mode and sum sales.  
**Explanation:** Shows sales mix by shipping choice.

### 11. State profit status

**Problem:** Label states as profitable or loss-making.  
**SQL:**

```sql
SELECT State,
       SUM(Profit) AS total_profit,
       CASE WHEN SUM(Profit) < 0
            THEN 'Loss-making'
            ELSE 'Profitable'
       END AS status
FROM retail_data
GROUP BY State;
```

**Expected logic:** Use `CASE` after aggregation.  
**Explanation:** Converts profit into a business status.

### 12. Category and sub-category summary

**Problem:** Summarize sales and profit by both product hierarchy levels.  
**SQL:**

```sql
SELECT Category, "Sub-Category",
       SUM(Sales) AS total_sales,
       SUM(Profit) AS total_profit
FROM retail_data
GROUP BY Category, "Sub-Category"
ORDER BY total_profit DESC;
```

**Expected logic:** Group by both dimensions.  
**Explanation:** Reveals detail hidden by category totals.

### 13. Segment-region performance

**Problem:** Compare profit by segment and region.  
**SQL:**

```sql
SELECT Segment, Region,
       SUM(Sales) AS sales,
       SUM(Profit) AS profit,
       SUM(Quantity) AS quantity
FROM retail_data
GROUP BY Segment, Region
ORDER BY profit DESC;
```

**Expected logic:** Create a two-dimensional grouped summary.  
**Explanation:** Finds strong combinations of segment and geography.

### 14. Records above average sales

**Problem:** Return transactions with sales above the overall average.  
**SQL:**

```sql
SELECT *
FROM retail_data
WHERE Sales > (SELECT AVG(Sales) FROM retail_data);
```

**Expected logic:** Compare each row to a scalar subquery.  
**Explanation:** Identifies larger-than-average transactions.

### 15. Profit margin by discount range

**Problem:** Compare profitability across discount bands.  
**SQL:**

```sql
SELECT CASE
           WHEN Discount = 0 THEN '0%'
           WHEN Discount <= 0.10 THEN '1-10%'
           WHEN Discount <= 0.20 THEN '11-20%'
           WHEN Discount <= 0.30 THEN '21-30%'
           ELSE '31%+'
       END AS discount_range,
       SUM(Sales) AS sales,
       SUM(Profit) AS profit,
       100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0) AS profit_margin
FROM retail_data
GROUP BY CASE
           WHEN Discount = 0 THEN '0%'
           WHEN Discount <= 0.10 THEN '1-10%'
           WHEN Discount <= 0.20 THEN '11-20%'
           WHEN Discount <= 0.30 THEN '21-30%'
           ELSE '31%+'
         END
ORDER BY profit_margin DESC;
```

**Expected logic:** Bucket discounts, aggregate measures, calculate margin.  
**Explanation:** Evaluates the commercial effect of discount levels.

## 10. Twenty-Five Common SQL Interview Questions

### Beginner

1. **What is SQL?**  
   SQL is a language for querying and managing relational data.
2. **What is the difference between `WHERE` and `HAVING`?**  
   `WHERE` filters rows; `HAVING` filters groups after aggregation.
3. **What does `DISTINCT` do?**  
   It removes duplicate result values.
4. **What does `NULL` mean?**  
   It represents missing or unknown data.
5. **How do you sort results?**  
   Use `ORDER BY`, followed by a column and optional `ASC` or `DESC`.
6. **What does `GROUP BY` do?**  
   It combines rows into groups for aggregation.
7. **What is a primary key?**  
   A unique, non-NULL identifier for a row.
8. **What is an inner join?**  
   It returns only matching rows from both tables.

### Intermediate

9. **What is a left join?**  
   It keeps every left-table row and matching right-table data.
10. **What is the difference between `COUNT(*)` and `COUNT(column)`?**  
    `COUNT(*)` counts rows; `COUNT(column)` excludes NULL values.
11. **How do you find duplicates?**  
    Group by the identifying columns and use `HAVING COUNT(*) > 1`.
12. **What is a subquery?**  
    A query nested inside another query.
13. **What is a CTE?**  
    A named temporary query defined with `WITH`.
14. **What is a calculated column?**  
    A value derived from existing columns using an expression.
15. **How do you avoid division by zero?**  
    Use `NULLIF(denominator, 0)`.
16. **What is a CASE expression?**  
    Conditional logic that returns a value based on rules.
17. **How do you find the second-highest value?**  
    Use a ranking function or a subquery excluding the maximum.

### Advanced

18. **What is a window function?**  
    It calculates across related rows without collapsing them.
19. **What is the difference between `RANK` and `DENSE_RANK`?**  
    Both tie, but `RANK` leaves gaps while `DENSE_RANK` does not.
20. **When would you use `ROW_NUMBER`?**  
    When every row needs a unique sequential number.
21. **What does `PARTITION BY` do?**  
    It resets a window calculation for each group.
22. **What is a correlated subquery?**  
    A subquery that refers to values from the outer query.
23. **What is the difference between `UNION` and `UNION ALL`?**  
    `UNION` removes duplicates; `UNION ALL` preserves them and is usually faster.
24. **What is the difference between `DELETE`, `TRUNCATE`, and `DROP`?**  
    `DELETE` removes selected rows, `TRUNCATE` removes all rows, and `DROP` removes the table structure.
25. **Subquery or join: which is better?**  
    It depends on clarity, database optimizer behavior, and the problem. Both can solve similar tasks.

## 11. SQL Challenges

### Problems

1. Return total sales and profit for every region.
2. Find the three most profitable sub-categories.
3. Find states whose total profit is negative.
4. Calculate profit margin by segment.
5. Count records by shipping mode.
6. Return cities with more than 100 records.
7. Find categories with average discount above 20%.
8. Return the highest-profit state in each region.
9. Rank sub-categories within each category by profit.
10. Calculate a running total of regional sales alphabetically by region.

### Answers

```sql
-- 1
SELECT Region, SUM(Sales) AS sales, SUM(Profit) AS profit
FROM retail_data GROUP BY Region;

-- 2
SELECT "Sub-Category", SUM(Profit) AS profit
FROM retail_data GROUP BY "Sub-Category"
ORDER BY profit DESC LIMIT 3;

-- 3
SELECT State, SUM(Profit) AS profit
FROM retail_data GROUP BY State
HAVING SUM(Profit) < 0;

-- 4
SELECT Segment,
       100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0) AS profit_margin
FROM retail_data GROUP BY Segment;

-- 5
SELECT "Ship Mode", COUNT(*) AS records
FROM retail_data GROUP BY "Ship Mode";

-- 6
SELECT City, COUNT(*) AS records
FROM retail_data GROUP BY City
HAVING COUNT(*) > 100;

-- 7
SELECT Category, AVG(Discount) AS average_discount
FROM retail_data GROUP BY Category
HAVING AVG(Discount) > 0.20;

-- 8
WITH state_profit AS (
    SELECT Region, State, SUM(Profit) AS profit
    FROM retail_data GROUP BY Region, State
), ranked AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY Region ORDER BY profit DESC
    ) AS rn
    FROM state_profit
)
SELECT Region, State, profit
FROM ranked WHERE rn = 1;

-- 9
WITH p AS (
    SELECT Category, "Sub-Category", SUM(Profit) AS profit
    FROM retail_data GROUP BY Category, "Sub-Category"
)
SELECT *, RANK() OVER (
    PARTITION BY Category ORDER BY profit DESC
) AS profit_rank
FROM p;

-- 10
WITH r AS (
    SELECT Region, SUM(Sales) AS sales
    FROM retail_data GROUP BY Region
)
SELECT Region, sales,
       SUM(sales) OVER (ORDER BY Region) AS running_sales
FROM r;
```

## 12. Important Concept Differences

| Concept | Difference |
|---|---|
| `WHERE` vs `HAVING` | `WHERE` filters rows before grouping; `HAVING` filters aggregated groups. |
| `GROUP BY` vs `ORDER BY` | `GROUP BY` forms summary groups; `ORDER BY` sorts the output. |
| `RANK` vs `DENSE_RANK` vs `ROW_NUMBER` | `RANK` ties with gaps; `DENSE_RANK` ties without gaps; `ROW_NUMBER` never ties. |
| `INNER JOIN` vs `LEFT JOIN` | Inner keeps matches only; left keeps every left-side row. |
| `UNION` vs `UNION ALL` | Union removes duplicates; Union All keeps all rows. |
| `DELETE` vs `TRUNCATE` vs `DROP` | Delete removes rows selectively; truncate clears rows; drop removes the table. |
| `COUNT(*)` vs `COUNT(column)` | Count star includes rows with NULLs; count column excludes NULL in that column. |
| Subquery vs JOIN | A subquery nests logic; a join combines tables. Choose the clearer and more efficient approach. |

## 13. Interview Cheat Sheet

```sql
SELECT columns
FROM table
WHERE condition
GROUP BY columns
HAVING aggregate_condition
ORDER BY column DESC
LIMIT 10;
```

- Filter rows with `WHERE`.
- Filter aggregates with `HAVING`.
- Use `SUM`, `AVG`, `COUNT`, `MIN`, and `MAX` for summaries.
- Always group non-aggregated selected columns.
- Use `NULLIF(value, 0)` for safe division.
- Use `CASE WHEN` for business categories and flags.
- Use joins to combine related tables.
- Use CTEs to make complex queries readable.
- Use window functions for rankings, running totals, and comparisons without losing row detail.
- Use `ROW_NUMBER()` for top-N per group when exactly one row per rank is needed.
- Check NULL behavior in comparisons and aggregates.
- Use `EXPLAIN` when investigating query performance.
- Validate results with totals, row counts, and a few manual examples.

For this project, remember: the dataset supports sales, profit, quantity, discount, product hierarchy, geography, segment, and shipping analysis. It does not support customer-level or date-level SQL analysis.

**SQL INTERVIEW MODULE: COMPLETE**
