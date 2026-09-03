"""Retail Business Analysis Portfolio Project

This script builds a professional data analysis workflow for the
SampleSuperstore.csv dataset. It performs data cleaning, KPI analysis,
dashboard creation, advanced business analysis, and outputs charts and CSVs.

Key notes:
- The dataset does not include a unique customer ID or order ID column.
- Therefore, each row is treated as one order for KPI purposes.
- Product analysis is performed using the available Sub-Category dimension,
  because there is no individual product name column in the source file.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", context="notebook")

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "SampleSuperstore.csv"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CHARTS_DIR = OUTPUTS_DIR / "charts"


def print_section(title: str) -> None:
    """Print a clear section title."""
    print(f"\n{'=' * 90}\n{title}\n{'=' * 90}")


def ensure_output_folders() -> None:
    """Create output folders if they do not exist."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)


def save_plot(fig: plt.Figure, filename: str) -> None:
    """Save a figure to the charts folder."""
    ensure_output_folders()
    fig.savefig(CHARTS_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close(fig)


def save_csv(df: pd.DataFrame, filename: str) -> None:
    """Save a DataFrame to the outputs folder."""
    ensure_output_folders()
    df.to_csv(OUTPUTS_DIR / filename, index=False)


def load_data(file_path: Path) -> pd.DataFrame:
    """Load the CSV with proper error handling."""
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    try:
        df = pd.read_csv(file_path)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Could not read the dataset file: {file_path}") from exc

    if df.empty:
        raise ValueError("The dataset is empty. Please check the CSV file.")

    return df


def inspect_dataset(df: pd.DataFrame) -> None:
    """Show a quick overview of the raw dataset."""
    print_section("1. DATASET INSPECTION")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Data types:\n{df.dtypes.to_string()}")
    print("\nFirst 5 rows:")
    print(df.head().to_string(index=False))


def data_quality_checks(df: pd.DataFrame) -> None:
    """Perform a complete quality audit on the raw dataset."""
    print_section("2. DATA QUALITY CHECKS")

    print("Missing values by column:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("No missing values found.")
    else:
        print(missing[missing > 0].to_string())

    duplicate_rows = int(df.duplicated().sum())
    print(f"\nDuplicate rows: {duplicate_rows}")

    print("\nNumeric validation checks:")
    for column in ["Sales", "Quantity", "Discount", "Profit"]:
        if column in df.columns:
            series = pd.to_numeric(df[column], errors="coerce")
            invalid = int(series.isna().sum())
            negative = int((series < 0).sum())
            if column == "Profit":
                print(f"- {column}: {negative} negative values (valid losses), {invalid} invalid values found.")
            else:
                print(f"- {column}: {negative} negative values, {invalid} invalid values found.")

    print("\nData type summary:")
    print(df.info())


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates and clean invalid values while preserving business logic."""
    print_section("3. DATA CLEANING")

    before_rows = df.shape[0]
    before_columns = df.shape[1]
    before_missing = int(df.isnull().sum().sum())
    before_duplicates = int(df.duplicated().sum())

    print("Before cleaning summary:")
    clean_summary = pd.DataFrame(
        [{
            "Rows": before_rows,
            "Columns": before_columns,
            "Missing Values": before_missing,
            "Duplicate Rows": before_duplicates,
        }]
    )
    print(clean_summary.to_string(index=False))

    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    print(f"Duplicate rows removed: {before_duplicates}")

    date_candidates = ["Order Date", "Order_Date", "order_date", "Date", "date"]
    for column in date_candidates:
        if column in cleaned.columns:
            cleaned[column] = pd.to_datetime(cleaned[column], errors="coerce")
            invalid_dates = int(cleaned[column].isna().sum())
            if invalid_dates:
                print(f"{invalid_dates} invalid values in '{column}' converted to NaT.")

    numeric_columns = ["Sales", "Quantity", "Discount", "Profit", "Postal Code"]
    for column in numeric_columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    for column in ["Sales", "Quantity", "Discount"]:
        if column in cleaned.columns:
            negative_count = int((cleaned[column] < 0).sum())
            if negative_count > 0:
                print(f"Negative values found in '{column}'; replacing them with NaN.")
                cleaned.loc[cleaned[column] < 0, column] = np.nan

    required_numeric = [column for column in ["Sales", "Quantity", "Discount", "Profit"] if column in cleaned.columns]
    if required_numeric:
        cleaned = cleaned.dropna(subset=required_numeric).reset_index(drop=True)

    if "Postal Code" in cleaned.columns:
        cleaned = cleaned.dropna(subset=["Postal Code"]).reset_index(drop=True)

    after_rows = cleaned.shape[0]
    after_columns = cleaned.shape[1]
    after_missing = int(cleaned.isnull().sum().sum())
    after_duplicates = int(cleaned.duplicated().sum())

    print("\nAfter cleaning summary:")
    after_summary = pd.DataFrame(
        [{
            "Rows": after_rows,
            "Columns": after_columns,
            "Missing Values": after_missing,
            "Duplicate Rows": after_duplicates,
        }]
    )
    print(after_summary.to_string(index=False))

    print("\nCleaned data preview:")
    print(cleaned.head().to_string(index=False))

    return cleaned


def format_currency(value: float) -> str:
    """Return a formatted currency string."""
    return f"${value:,.2f}"


def format_percentage(value: float) -> str:
    """Return a percentage string."""
    return f"{value:.2f}%"


def get_order_definition() -> str:
    """Explain the order definition based on the dataset structure."""
    return (
        "Each row is treated as one order because the dataset does not contain a unique order ID or customer ID column. "
        "This is the most appropriate unit available from the source data."
    )


def calculate_kpis(df: pd.DataFrame) -> dict:
    """Compute key business KPI metrics from the cleaned dataset."""
    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    total_orders = int(len(df))
    total_quantity = int(df["Quantity"].sum())
    average_order_value = total_sales / total_orders if total_orders else 0.0
    profit_margin = (total_profit / total_sales * 100) if total_sales else 0.0

    if "Customer ID" in df.columns:
        total_customers = int(df["Customer ID"].nunique())
    else:
        total_customers = None

    if "Sub-Category" in df.columns:
        total_products = int(df["Sub-Category"].nunique())
    else:
        total_products = 0

    return {
        "Total Sales": total_sales,
        "Total Profit": total_profit,
        "Total Orders": total_orders,
        "Total Quantity Sold": total_quantity,
        "Average Order Value": average_order_value,
        "Profit Margin": profit_margin,
        "Number of Customers": total_customers,
        "Number of Products": total_products,
    }


def print_kpi_summary(kpis: dict) -> None:
    """Print KPI summary to the console."""
    print_section("4. KPI SUMMARY")
    print(get_order_definition())
    rows = [
        ("Total Sales", format_currency(kpis["Total Sales"])),
        ("Total Profit", format_currency(kpis["Total Profit"])),
        ("Total Orders", f"{kpis['Total Orders']:,}"),
        ("Total Quantity Sold", f"{kpis['Total Quantity Sold']:,}"),
        ("Average Order Value", format_currency(kpis["Average Order Value"])),
        ("Profit Margin", format_percentage(kpis["Profit Margin"])),
        ("Number of Customers", "N/A - no customer identifier in dataset" if kpis["Number of Customers"] is None else f"{kpis['Number of Customers']:,}"),
        ("Number of Products", f"{kpis['Number of Products']:,}"),
    ]
    for label, value in rows:
        print(f"{label:<25} {value}")


def create_kpi_dashboard(kpis: dict) -> None:
    """Create a dashboard-style KPI summary using Matplotlib."""
    print_section("5. PROFESSIONAL KPI DASHBOARD")

    customer_value = "N/A" if kpis["Number of Customers"] is None else f"{kpis['Number of Customers']:,}"
    cards = [
        ("Total Sales", format_currency(kpis["Total Sales"])),
        ("Total Profit", format_currency(kpis["Total Profit"])),
        ("Total Orders", f"{kpis['Total Orders']:,}"),
        ("Total Quantity", f"{kpis['Total Quantity Sold']:,}"),
        ("Average Order Value", format_currency(kpis["Average Order Value"])),
        ("Profit Margin", format_percentage(kpis["Profit Margin"])),
        ("Customers", customer_value),
        ("Products", f"{kpis['Number of Products']:,}"),
    ]

    fig, axes = plt.subplots(2, 4, figsize=(18, 9))
    fig.suptitle("Retail Business KPI Dashboard", fontsize=20, fontweight="bold", y=0.98)

    for ax in axes.flat:
        ax.set_facecolor("#f7f9fc")
        ax.set_axis_off()

    colors = [
        "#1f4e79", "#2e7d32", "#6a4c93", "#ef6c00",
        "#00796b", "#c62828", "#455a64", "#8e24aa"
    ]

    for idx, (label, value) in enumerate(cards):
        ax = axes.flat[idx]
        ax.set_facecolor("#ffffff")
        ax.patch.set_edgecolor(colors[idx % len(colors)])
        ax.patch.set_linewidth(1.5)
        ax.annotate(label, xy=(0.5, 0.75), textcoords="axes fraction", ha="center", va="center",
                    fontsize=12, fontweight="bold", color="#263238")
        ax.annotate(value, xy=(0.5, 0.35), textcoords="axes fraction", ha="center", va="center",
                    fontsize=20, fontweight="bold", color=colors[idx % len(colors)])

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    save_plot(fig, "kpi_dashboard.png")


def save_analysis_outputs(df: pd.DataFrame) -> None:
    """Generate and save required analysis output CSV files."""
    category_analysis = df.groupby("Category").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Sales", "size"),
    ).reset_index()
    save_csv(category_analysis, "category_analysis.csv")

    subcategory_analysis = df.groupby("Sub-Category").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("Sales", "size"),
    ).reset_index()
    save_csv(subcategory_analysis, "subcategory_analysis.csv")

    region_analysis = df.groupby("Region").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Sales", "size"),
    ).reset_index()
    save_csv(region_analysis, "region_analysis.csv")

    product_analysis = df.groupby("Sub-Category").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
    ).reset_index()
    save_csv(product_analysis, "product_analysis.csv")

    state_analysis = df.groupby("State").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Sales", "size"),
    ).reset_index()
    save_csv(state_analysis, "state_analysis.csv")

    discount_bins = [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 1.00]
    labels = ["0-10%", "10-20%", "20-30%", "30-40%", "40-50%", "50-60%", "60-100%"]
    discount_df = df.copy()
    discount_df["Discount Range"] = pd.cut(discount_df["Discount"], bins=discount_bins, labels=labels, right=False)
    discount_analysis = discount_df.groupby("Discount Range").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Sales", "size"),
    ).reset_index()
    save_csv(discount_analysis, "discount_analysis.csv")

    if "Customer ID" in df.columns:
        customer_analysis = df.groupby("Customer ID").agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Sales", "size"),
        ).reset_index()
        save_csv(customer_analysis, "customer_analysis.csv")
    else:
        save_csv(pd.DataFrame({"Note": ["Customer identifier is not available in the source dataset."]}), "customer_analysis.csv")

    date_cols = [col for col in ["Order Date", "Order_Date", "order_date", "Date", "date"] if col in df.columns]
    if date_cols:
        date_col = date_cols[0]
        time_df = df[[date_col, "Sales", "Profit"]].copy()
        time_df[date_col] = pd.to_datetime(time_df[date_col], errors="coerce")
        time_df = time_df.dropna(subset=[date_col]).copy()
        time_df["Month"] = time_df[date_col].dt.to_period("M").dt.to_timestamp()
        monthly_sales = time_df.groupby("Month")["Sales"].sum().reset_index()
        monthly_profit = time_df.groupby("Month")["Profit"].sum().reset_index()
        monthly_orders = time_df.groupby("Month").size().reset_index(name="Orders")
        save_csv(monthly_sales, "monthly_sales.csv")
        save_csv(monthly_profit, "monthly_profit.csv")
        save_csv(monthly_orders, "monthly_orders.csv")
    else:
        note_df = pd.DataFrame({"Note": ["No date column is available in the source dataset, so monthly analysis is unavailable."]})
        save_csv(note_df, "monthly_sales.csv")
        save_csv(note_df.copy(), "monthly_profit.csv")
        save_csv(note_df.copy(), "monthly_orders.csv")


def plot_bar_chart(data: pd.DataFrame, x_col: str, y_col: str, title: str, x_label: str, y_label: str, filename: str, top_n: int | None = None, ascending: bool = False) -> None:
    """Create a professional bar chart."""
    plot_data = data.copy()
    if top_n is not None:
        plot_data = plot_data.head(top_n)
    if ascending:
        plot_data = plot_data.sort_values(by=y_col, ascending=True)
    else:
        plot_data = plot_data.sort_values(by=y_col, ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=plot_data, x=x_col, y=y_col, palette="viridis", ax=ax)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    save_plot(fig, filename)


def plot_segment_analysis(df: pd.DataFrame) -> None:
    """Create a segment analysis chart for sales and profit."""
    segment_summary = df.groupby("Segment").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    sns.barplot(data=segment_summary, x="Segment", y="Sales", palette="Blues_d", ax=axes[0])
    axes[0].set_title("Sales by Segment")
    axes[0].set_xlabel("Segment")
    axes[0].set_ylabel("Sales")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)

    sns.barplot(data=segment_summary, x="Segment", y="Profit", palette="Greens_d", ax=axes[1])
    axes[1].set_title("Profit by Segment")
    axes[1].set_xlabel("Segment")
    axes[1].set_ylabel("Profit")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    save_plot(fig, "segment_analysis.png")


def plot_discount_vs_profit(df: pd.DataFrame) -> None:
    """Plot the relationship between discount and profit."""
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.scatterplot(data=df, x="Discount", y="Profit", alpha=0.7, ax=ax)
    sns.regplot(data=df, x="Discount", y="Profit", scatter=False, color="crimson", ax=ax)
    ax.set_title("Discount vs Profit")
    ax.set_xlabel("Discount")
    ax.set_ylabel("Profit")
    ax.grid(True, linestyle="--", alpha=0.3)
    fig.tight_layout()
    save_plot(fig, "discount_profit.png")


def plot_time_analysis(df: pd.DataFrame) -> None:
    """Create monthly and yearly sales/profit charts when a date column exists."""
    date_candidates = ["Order Date", "Order_Date", "order_date", "Date", "date"]
    date_col = next((col for col in date_candidates if col in df.columns), None)
    if date_col is None:
        print("\nTime analysis is unavailable because the source dataset does not contain a valid date column.")
        return

    time_df = df[[date_col, "Sales", "Profit", "Quantity"]].copy()
    time_df[date_col] = pd.to_datetime(time_df[date_col], errors="coerce")
    time_df = time_df.dropna(subset=[date_col]).copy()

    time_df["Month"] = time_df[date_col].dt.to_period("M").dt.to_timestamp()
    time_df["Year"] = time_df[date_col].dt.year

    monthly_sales = time_df.groupby("Month")["Sales"].sum().reset_index()
    monthly_profit = time_df.groupby("Month")["Profit"].sum().reset_index()
    monthly_orders = time_df.groupby("Month").size().reset_index(name="Orders")
    yearly_sales = time_df.groupby("Year")["Sales"].sum().reset_index()
    yearly_profit = time_df.groupby("Year")["Profit"].sum().reset_index()

    print_section("6. TIME ANALYSIS")
    print("Monthly Sales:\n", monthly_sales.head(12).to_string(index=False))
    print("\nMonthly Profit:\n", monthly_profit.head(12).to_string(index=False))
    print("\nMonthly Orders:\n", monthly_orders.head(12).to_string(index=False))
    print("\nYearly Sales:\n", yearly_sales.to_string(index=False))
    print("\nYearly Profit:\n", yearly_profit.to_string(index=False))

    best_month = monthly_sales.loc[monthly_sales["Sales"].idxmax()]
    best_year = yearly_sales.loc[yearly_sales["Sales"].idxmax()]
    print(f"\nBest-performing month: {best_month['Month'].strftime('%Y-%m')} with sales of {format_currency(best_month['Sales'])}.")
    print(f"Best-performing year: {best_year['Year']} with sales of {format_currency(best_year['Sales'])}.")

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    sns.lineplot(data=monthly_sales, x="Month", y="Sales", marker="o", ax=axes[0], color="tab:blue")
    axes[0].set_title("Monthly Sales")
    axes[0].set_xlabel("Month")
    axes[0].set_ylabel("Sales")
    axes[0].grid(True, linestyle="--", alpha=0.3)

    sns.lineplot(data=monthly_profit, x="Month", y="Profit", marker="o", ax=axes[1], color="tab:green")
    axes[1].set_title("Monthly Profit")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Profit")
    axes[1].grid(True, linestyle="--", alpha=0.3)

    fig.tight_layout()
    save_plot(fig, "monthly_sales_profit.png")

    fig_year, axes_year = plt.subplots(2, 1, figsize=(10, 8))
    sns.barplot(data=yearly_sales, x="Year", y="Sales", palette="viridis", ax=axes_year[0])
    axes_year[0].set_title("Yearly Sales")
    axes_year[0].set_xlabel("Year")
    axes_year[0].set_ylabel("Sales")

    sns.barplot(data=yearly_profit, x="Year", y="Profit", palette="magma", ax=axes_year[1])
    axes_year[1].set_title("Yearly Profit")
    axes_year[1].set_xlabel("Year")
    axes_year[1].set_ylabel("Profit")

    fig_year.tight_layout()
    save_plot(fig_year, "yearly_sales_profit.png")


def perform_customer_analysis(df: pd.DataFrame) -> None:
    """Customer analysis based on available customer fields. If absent, document it clearly."""
    print_section("7. CUSTOMER ANALYSIS")
    customer_columns = [col for col in df.columns if "customer" in col.lower()]

    if not customer_columns:
        print("No customer identifier is available in the current dataset. Customer-level analysis cannot be performed without a Customer ID or Customer Name column.")
        return

    customer_col = customer_columns[0]
    customer_summary = df.groupby(customer_col).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Sales", "size"),
    ).reset_index()

    top_customers_sales = customer_summary.sort_values("Sales", ascending=False).head(10)
    top_customers_profit = customer_summary.sort_values("Profit", ascending=False).head(10)
    loss_customers = customer_summary[customer_summary["Profit"] < 0]

    print(f"Number of unique customers: {customer_summary.shape[0]}")
    print("\nTop 10 customers by Sales:")
    print(top_customers_sales.to_string(index=False))
    print("\nTop 10 customers by Profit:")
    print(top_customers_profit.to_string(index=False))
    print("\nCustomers generating losses:")
    if loss_customers.empty:
        print("No customers are generating losses.")
    else:
        print(loss_customers.head(10).to_string(index=False))

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    sns.barplot(data=top_customers_sales, x="Sales", y=customer_col, palette="Blues_d", ax=axes[0])
    axes[0].set_title("Top 10 Customers by Sales")
    axes[0].set_xlabel("Sales")
    axes[0].set_ylabel(customer_col)

    sns.barplot(data=top_customers_profit, x="Profit", y=customer_col, palette="Greens_d", ax=axes[1])
    axes[1].set_title("Top 10 Customers by Profit")
    axes[1].set_xlabel("Profit")
    axes[1].set_ylabel(customer_col)

    fig.tight_layout()
    save_plot(fig, "customer_analysis.png")


def perform_product_analysis(df: pd.DataFrame) -> None:
    """Analyze products using the available sub-category dimension."""
    print_section("8. PRODUCT ANALYSIS")

    product_summary = df.groupby("Sub-Category").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum"),
    ).reset_index()

    top_sales_products = product_summary.sort_values("Sales", ascending=False).head(10)
    top_profit_products = product_summary.sort_values("Profit", ascending=False).head(10)
    bottom_profit_products = product_summary.sort_values("Profit", ascending=True).head(10)
    top_quantity_products = product_summary.sort_values("Quantity", ascending=False).head(10)
    high_sales_negative_profit = product_summary[(product_summary["Sales"] >= product_summary["Sales"].quantile(0.75)) & (product_summary["Profit"] < 0)]

    print("Top 10 products by Sales:")
    print(top_sales_products.to_string(index=False))
    print("\nTop 10 products by Profit:")
    print(top_profit_products.to_string(index=False))
    print("\nBottom 10 products by Profit:")
    print(bottom_profit_products.to_string(index=False))
    print("\nTop products by Quantity:")
    print(top_quantity_products.to_string(index=False))
    print("\nProducts with high sales but negative profit:")
    if high_sales_negative_profit.empty:
        print("No products meet this high-sales and negative-profit criterion.")
    else:
        print(high_sales_negative_profit.to_string(index=False))

    plot_bar_chart(top_sales_products, "Sub-Category", "Sales", "Top 10 Products by Sales", "Product", "Sales", "top_products_sales.png")
    plot_bar_chart(top_profit_products, "Sub-Category", "Profit", "Top 10 Products by Profit", "Product", "Profit", "top_products_profit.png")
    plot_bar_chart(bottom_profit_products, "Sub-Category", "Profit", "Bottom 10 Products by Profit", "Product", "Profit", "bottom_products_profit.png", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_quantity_products, x="Quantity", y="Sub-Category", palette="magma", ax=ax)
    ax.set_title("Top Products by Quantity")
    ax.set_xlabel("Quantity")
    ax.set_ylabel("Sub-Category")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    fig.tight_layout()
    save_plot(fig, "top_products_quantity.png")


def perform_geographical_analysis(df: pd.DataFrame) -> None:
    """Analyze sales and profit by state and region."""
    print_section("9. GEOGRAPHICAL ANALYSIS")

    state_sales = df.groupby("State")["Sales"].sum().sort_values(ascending=False).reset_index().rename(columns={"Sales": "Total Sales"})
    state_profit = df.groupby("State")["Profit"].sum().sort_values(ascending=False).reset_index().rename(columns={"Profit": "Total Profit"})
    bottom_state_profit = df.groupby("State")["Profit"].sum().sort_values(ascending=True).reset_index().rename(columns={"Profit": "Total Profit"})

    print("Top 10 states by Sales:")
    print(state_sales.head(10).to_string(index=False))
    print("\nTop 10 states by Profit:")
    print(state_profit.head(10).to_string(index=False))
    print("\nBottom 10 states by Profit:")
    print(bottom_state_profit.head(10).to_string(index=False))

    plot_bar_chart(state_sales.head(10), "State", "Total Sales", "Top 10 States by Sales", "State", "Sales", "state_sales.png")
    plot_bar_chart(state_profit.head(10), "State", "Total Profit", "Top 10 States by Profit", "State", "Profit", "state_profit.png")

    region_summary = df.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    sns.barplot(data=region_summary, x="Region", y="Sales", palette="viridis", ax=axes[0])
    axes[0].set_title("Sales by Region")
    axes[0].set_xlabel("Region")
    axes[0].set_ylabel("Sales")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)

    sns.barplot(data=region_summary, x="Region", y="Profit", palette="magma", ax=axes[1])
    axes[1].set_title("Profit by Region")
    axes[1].set_xlabel("Region")
    axes[1].set_ylabel("Profit")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)

    fig.tight_layout()
    save_plot(fig, "region_analysis.png")


def perform_discount_analysis(df: pd.DataFrame) -> None:
    """Group discounts into ranges and assess their financial impact."""
    print_section("10. DISCOUNT ANALYSIS")

    bins = [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 1.00]
    labels = ["0-10%", "10-20%", "20-30%", "30-40%", "40-50%", "50-60%", "60-100%"]
    discount_df = df.copy()
    discount_df["Discount Range"] = pd.cut(discount_df["Discount"], bins=bins, labels=labels, right=False)

    discount_summary = discount_df.groupby("Discount Range").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Sales", "size"),
    ).reset_index()

    print(discount_summary.to_string(index=False))
    corr = df["Discount"].corr(df["Profit"])
    print(f"\nDiscount vs Profit correlation: {corr:.4f}")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=discount_summary, x="Discount Range", y="Profit", palette="coolwarm", ax=ax)
    ax.set_title("Profit by Discount Range")
    ax.set_xlabel("Discount Range")
    ax.set_ylabel("Profit")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    plt.xticks(rotation=45)
    fig.tight_layout()
    save_plot(fig, "discount_profit_range.png")

    plot_discount_vs_profit(df)


def perform_sales_vs_profit_analysis(df: pd.DataFrame) -> None:
    """Compare product-level sales and profit to identify high/low performers."""
    print_section("11. SALES VS PROFIT ANALYSIS")

    product_summary = df.groupby("Sub-Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
    sales_mid = product_summary["Sales"].median()
    profit_mid = product_summary["Profit"].median()

    product_summary["Category"] = np.where(
        (product_summary["Sales"] >= sales_mid) & (product_summary["Profit"] >= profit_mid),
        "High Sales + High Profit",
        np.where(
            (product_summary["Sales"] >= sales_mid) & (product_summary["Profit"] < profit_mid),
            "High Sales + Low Profit",
            np.where(
                (product_summary["Sales"] < sales_mid) & (product_summary["Profit"] >= profit_mid),
                "Low Sales + High Profit",
                "Low Sales + Negative Profit",
            ),
        ),
    )

    for label in ["High Sales + High Profit", "High Sales + Low Profit", "Low Sales + High Profit", "Low Sales + Negative Profit"]:
        entries = product_summary[product_summary["Category"] == label]
        if entries.empty:
            print(f"{label}: no products identified.")
        else:
            print(f"\n{label}:")
            print(entries[["Sub-Category", "Sales", "Profit"]].to_string(index=False))

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.scatterplot(data=product_summary, x="Sales", y="Profit", hue="Category", s=120, palette="Set2", ax=ax)
    ax.set_title("Sales vs Profit by Sub-Category")
    ax.set_xlabel("Sales")
    ax.set_ylabel("Profit")
    ax.grid(True, linestyle="--", alpha=0.3)
    fig.tight_layout()
    save_plot(fig, "sales_vs_profit.png")


def generate_business_summary(df: pd.DataFrame, kpis: dict) -> list[str]:
    """Build a final summary based strictly on calculated results."""
    category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    category_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
    region_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
    subcategory_profit = df.groupby("Sub-Category")["Profit"].sum().sort_values(ascending=True)
    segment_sales = df.groupby("Segment")["Sales"].sum().sort_values(ascending=False)
    discount_corr = df["Discount"].corr(df["Profit"])

    insights = [
        f"The highest-performing category is {category_sales.index[0]} with {format_currency(category_sales.iloc[0])} in sales.",
        f"The most profitable category is {category_profit.index[0]} with {format_currency(category_profit.iloc[0])} in profit.",
        f"The most profitable region is {region_profit.index[0]} with {format_currency(region_profit.iloc[0])} in profit.",
        f"The biggest loss-making sub-category is {subcategory_profit.index[0]} with {format_currency(subcategory_profit.iloc[0])} in profit.",
        f"The strongest customer segment is {segment_sales.index[0]} with {format_currency(segment_sales.iloc[0])} in sales.",
        f"The discount analysis indicates a negative relationship between discounts and profit (correlation: {discount_corr:.4f}), suggesting high discounting is associated with lower profit.",
        f"The top product by sales is {df.groupby('Sub-Category')['Sales'].sum().idxmax()} with {format_currency(df.groupby('Sub-Category')['Sales'].sum().max())} in sales.",
        f"The top product by profit is {df.groupby('Sub-Category')['Profit'].sum().idxmax()} with {format_currency(df.groupby('Sub-Category')['Profit'].sum().max())} in profit.",
    ]
    return insights


def business_recommendations(df: pd.DataFrame) -> list[str]:
    """Create actionable recommendations based on the actual findings."""
    category_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
    region_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
    product_summary = df.groupby("Sub-Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
    worst_products = product_summary.sort_values("Profit", ascending=True).head(3)
    discount_corr = df["Discount"].corr(df["Profit"])

    recs = [
        f"Focus more promotional and inventory resources on {category_profit.index[0]} because it is the most profitable category and drives the strongest returns.",
        f"Review low-margin or loss-making sub-categories such as {', '.join(worst_products['Sub-Category'].tolist())} to reduce profit leakage and rationalize inventory.",
        f"Use a tighter discount strategy because discount levels show a negative relationship with profit (correlation: {discount_corr:.4f}).",
        f"Prioritize {region_profit.index[0]} and {region_profit.index[1]} for growth campaigns because they generate the highest profit across regions.",
        f"Promote top-selling products and bundle high-margin items where possible to increase average order value while maintaining profitability.",
        f"Review pricing and promotional structures for products with high sales and weak profit so they do not consume margin without enough return.",
        f"Monitor category-level profit trends regularly and track discounts by segment to keep profit margin stable over time.",
    ]
    return recs


def print_business_summary(df: pd.DataFrame, kpis: dict) -> None:
    """Print a final business summary and recommendations."""
    print_section("12. FINAL BUSINESS SUMMARY")
    insights = generate_business_summary(df, kpis)
    for item in insights:
        print(f"- {item}")

    print("\nRecommended actions:")
    recommendations = business_recommendations(df)
    for idx, rec in enumerate(recommendations, start=1):
        print(f"{idx}. {rec}")


def print_project_summary(kpis: dict, df: pd.DataFrame) -> None:
    """Print a concise project summary at the end of the run."""
    print_section("13. PROJECT SUMMARY")
    best_category = df.groupby("Category")["Sales"].sum().idxmax()
    best_region = df.groupby("Region")["Profit"].sum().idxmax()
    best_product = df.groupby("Sub-Category")["Sales"].sum().idxmax()
    worst_product = df.groupby("Sub-Category")["Profit"].sum().idxmin()

    customer_label = "N/A" if kpis["Number of Customers"] is None else f"{kpis['Number of Customers']:,}"

    print(f"Total Sales: {format_currency(kpis['Total Sales'])}")
    print(f"Total Profit: {format_currency(kpis['Total Profit'])}")
    print(f"Total Orders: {kpis['Total Orders']:,}")
    print(f"Total Customers: {customer_label}")
    print(f"Total Products: {kpis['Number of Products']:,}")
    print(f"Profit Margin: {format_percentage(kpis['Profit Margin'])}")
    print(f"Best Category: {best_category}")
    print(f"Best Region: {best_region}")
    print(f"Best Product: {best_product}")
    print(f"Worst Product: {worst_product}")


def main() -> None:
    """Run the full retail analytics workflow."""
    print("Starting retail analytics dashboard project...")

    try:
        raw_df = load_data(DATA_PATH)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}")
        return

    inspect_dataset(raw_df)
    data_quality_checks(raw_df)
    cleaned_df = clean_data(raw_df)

    if cleaned_df.empty:
        print("No valid rows remain after cleaning. Please review the dataset.")
        return

    cleaned_path = PROJECT_ROOT / "cleaned_superstore_data.csv"
    cleaned_df.to_csv(cleaned_path, index=False)
    print(f"\nCleaned dataset saved to: {cleaned_path}")

    kpis = calculate_kpis(cleaned_df)
    print_kpi_summary(kpis)
    create_kpi_dashboard(kpis)
    save_analysis_outputs(cleaned_df)

    plot_segment_analysis(cleaned_df)
    plot_discount_vs_profit(cleaned_df)
    plot_time_analysis(cleaned_df)
    perform_customer_analysis(cleaned_df)
    perform_product_analysis(cleaned_df)
    perform_geographical_analysis(cleaned_df)
    perform_discount_analysis(cleaned_df)
    perform_sales_vs_profit_analysis(cleaned_df)
    print_business_summary(cleaned_df, kpis)
    print_project_summary(kpis, cleaned_df)

    print(f"\nAll output files were saved to: {OUTPUTS_DIR}")
    print(f"Charts were saved to: {CHARTS_DIR}")


if __name__ == "__main__":
    main()
