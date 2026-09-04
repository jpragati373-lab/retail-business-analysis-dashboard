from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Business Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("📊 Retail Business Analytics")
st.success("Streamlit is running successfully!")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1500px; }
    [data-testid="stSidebar"] { background: #f7f9fc; border-right: 1px solid #e5e7eb; }
    [data-testid="stMetric"] {
        background: #ffffff; border: 1px solid #e5e7eb; border-radius: 14px;
        padding: 1rem 1.1rem; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }
    [data-testid="stMetricLabel"] { color: #64748b; font-size: 0.82rem; font-weight: 600; }
    [data-testid="stMetricValue"] { color: #0f172a; font-weight: 700; }
    h1 { letter-spacing: -0.04em; color: #0f172a; }
    h2, h3 { color: #1e293b; letter-spacing: -0.02em; margin-top: 1.4rem; }
    .portfolio-subtitle { color: #475569; font-size: 1.1rem; margin-top: -0.8rem; }
    .portfolio-kicker { color: #64748b; font-size: 0.85rem; margin-top: 0.25rem; }
    .health-card {
        background: #ffffff; border: 1px solid #dbe3ee; border-radius: 14px;
        padding: 1rem 1.25rem; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }
    .health-card strong { color: #0f172a; font-size: 1.05rem; }
    .analyst-takeaway {
        background: #f8fafc; border-left: 4px solid #2563eb; border-radius: 10px;
        padding: 1rem 1.1rem; color: #334155; line-height: 1.55;
    }
    .active-filters {
        background: #eef4ff; border: 1px solid #d7e4fb; border-radius: 10px;
        padding: 0.7rem 0.85rem; color: #334155; font-size: 0.85rem;
    }
    .section-divider { border-top: 1px solid #e5e7eb; margin: 1.5rem 0; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 2. DATA PATH
# ============================================================

DATA_PATH = Path(__file__).resolve().parent / "SampleSuperstore.csv"


# ============================================================
# 3. LOAD DATA
# ============================================================

@st.cache_data
def load_data(file_path):
    """Load the Superstore dataset."""

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    data = pd.read_csv(file_path)

    if data.empty:
        raise ValueError("The dataset is empty.")

    return data


# ============================================================
# 4. LOAD DATASET
# ============================================================

try:
    df = load_data(DATA_PATH)
except Exception as error:
    st.error(f"Unable to load dataset: {error}")
    st.stop()


# ============================================================
# 5. CLEAN DATA
# ============================================================

numeric_columns = ["Sales", "Quantity", "Discount", "Profit"]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")


df = df.dropna(how="all").reset_index(drop=True)


# ============================================================
# 6. HEADER
# ============================================================

st.title("Retail Business Analytics")
st.markdown('<div class="portfolio-subtitle">Interactive Sales &amp; Profitability Intelligence Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="portfolio-kicker">{len(df):,} retail transaction records analyzed</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    A polished, filterable view of sales, profit, discount behavior, customer
    segments, and regional performance.
    """
)
st.markdown("---")


# ============================================================
# 7. SIDEBAR FILTERS
# ============================================================

with st.sidebar:
    st.header("Dashboard Filters")
    st.caption("Explore the business dataset using the filters below.")

    with st.expander("Dataset Quality Report", expanded=False):
        st.write(f"Total rows: **{len(df):,}**")
        st.write(f"Total columns: **{len(df.columns):,}**")
        st.write(f"Missing values: **{df.isna().sum().sum():,}**")
        st.write(f"Duplicate rows: **{df.duplicated().sum():,}**")
        st.write(f"Number of states: **{df['State'].nunique() if 'State' in df.columns else 0:,}**")
        st.write(f"Number of cities: **{df['City'].nunique() if 'City' in df.columns else 0:,}**")
        st.write(f"Number of categories: **{df['Category'].nunique() if 'Category' in df.columns else 0:,}**")
        st.write(f"Number of sub-categories: **{df['Sub-Category'].nunique() if 'Sub-Category' in df.columns else 0:,}**")

    info_cols = st.columns(2)
    with info_cols[0]:
        st.metric(
            "Records",
            f"{len(df):,}",
            help="Total rows in the dataset."
        )

    with info_cols[1]:
        st.metric(
            "Columns",
            f"{len(df.columns):,}",
            help="Number of available columns in the dataset."
        )

    info_cols_2 = st.columns(2)
    with info_cols_2[0]:
        st.metric(
            "States",
            f"{df['State'].nunique() if 'State' in df.columns else 0:,}",
            help="Number of unique states present in the dataset."
        )

    with info_cols_2[1]:
        st.metric(
            "Cities",
            f"{df['City'].nunique() if 'City' in df.columns else 0:,}",
            help="Number of unique cities present in the dataset."
        )

    st.markdown("---")

    def build_filter(label, key_name, options):
        if key_name not in st.session_state:
            st.session_state[key_name] = "All"

        current_value = st.session_state[key_name]
        if current_value not in options:
            current_value = "All"
            st.session_state[key_name] = "All"

        return st.selectbox(
            label,
            options,
            index=options.index(current_value),
            key=key_name,
        )

    filter_keys = []

    if "Segment" in df.columns:
        segment_options = ["All"] + sorted(
            df["Segment"].dropna().astype(str).unique().tolist()
        )
        selected_segment = build_filter(
            "👥 Segment",
            "segment_filter",
            segment_options,
        )
        filter_keys.append("segment_filter")
    else:
        selected_segment = "All"

    if "Category" in df.columns:
        category_options = ["All"] + sorted(
            df["Category"].dropna().astype(str).unique().tolist()
        )
        selected_category = build_filter(
            "📦 Category",
            "category_filter",
            category_options,
        )
        filter_keys.append("category_filter")
    else:
        selected_category = "All"

    if "Sub-Category" in df.columns:
        subcategory_options = ["All"] + sorted(
            df["Sub-Category"].dropna().astype(str).unique().tolist()
        )
        selected_subcategory = build_filter(
            "📦 Sub-Category",
            "subcategory_filter",
            subcategory_options,
        )
        filter_keys.append("subcategory_filter")
    else:
        selected_subcategory = "All"

    if "Region" in df.columns:
        region_options = ["All"] + sorted(
            df["Region"].dropna().astype(str).unique().tolist()
        )
        selected_region = build_filter(
            "🌎 Region",
            "region_filter",
            region_options,
        )
        filter_keys.append("region_filter")
    else:
        selected_region = "All"

    if "State" in df.columns:
        state_options = ["All"] + sorted(
            df["State"].dropna().astype(str).unique().tolist()
        )
        selected_state = build_filter(
            "📍 State",
            "state_filter",
            state_options,
        )
        filter_keys.append("state_filter")
    else:
        selected_state = "All"

    if "Ship Mode" in df.columns:
        ship_options = ["All"] + sorted(
            df["Ship Mode"].dropna().astype(str).unique().tolist()
        )
        selected_ship_mode = build_filter(
            "🚚 Ship Mode",
            "ship_mode_filter",
            ship_options,
        )
        filter_keys.append("ship_mode_filter")
    else:
        selected_ship_mode = "All"

    st.markdown("---")

    if st.button("Reset Filters", width="stretch"):
        for key_name in filter_keys:
            st.session_state[key_name] = "All"
        st.rerun()

    st.markdown("**Active Filters**")
    st.markdown(
        '<div class="active-filters">'
        f"Segment: {selected_segment}<br>"
        f"Category: {selected_category}<br>"
        f"Sub-Category: {selected_subcategory}<br>"
        f"Region: {selected_region}<br>"
        f"State: {selected_state}<br>"
        f"Ship Mode: {selected_ship_mode}"
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# 8. APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_segment != "All" and "Segment" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Segment"] == selected_segment]

if selected_category != "All" and "Category" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if selected_subcategory != "All" and "Sub-Category" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Sub-Category"] == selected_subcategory]

if selected_region != "All" and "Region" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]

if selected_state != "All" and "State" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["State"] == selected_state]

if selected_ship_mode != "All" and "Ship Mode" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Ship Mode"] == selected_ship_mode]

filtered_df = filtered_df.reset_index(drop=True)


# ============================================================
# 9. EMPTY DATA CHECK
# ============================================================

if filtered_df.empty:
    st.warning("⚠️ No records match the selected filters. Please change the filters.")


# ============================================================
# 10. KPI CALCULATIONS
# ============================================================

total_sales = filtered_df["Sales"].sum() if "Sales" in filtered_df.columns else 0
total_profit = filtered_df["Profit"].sum() if "Profit" in filtered_df.columns else 0
total_quantity = filtered_df["Quantity"].sum() if "Quantity" in filtered_df.columns else 0
total_records = len(filtered_df)
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0
average_sales = total_sales / total_records if total_records > 0 else 0
total_cities = filtered_df["City"].nunique() if "City" in filtered_df.columns else 0
total_states = filtered_df["State"].nunique() if "State" in filtered_df.columns else 0
total_subcategories = filtered_df["Sub-Category"].nunique() if "Sub-Category" in filtered_df.columns else 0


# ============================================================
# 11. PLOT STYLE AND SUMMARY PREP
# ============================================================

def style_plot(fig, x_title=None, y_title=None):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Arial, sans-serif", size=12),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=10, r=10, t=40, b=10),
    )

    if x_title is not None:
        fig.update_xaxes(title_text=x_title)
    if y_title is not None:
        fig.update_yaxes(title_text=y_title)

    return fig


category_summary = None
subcategory_summary = None
region_summary = None
state_summary = None
city_summary = None
segment_summary = None
ship_summary = None
discount_summary = None
scatter_fig = None
correlation = None

if "Category" in filtered_df.columns:
    category_summary = (
        filtered_df.groupby("Category")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
        .reset_index()
    )

if "Sub-Category" in filtered_df.columns:
    subcategory_summary = (
        filtered_df.groupby("Sub-Category")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
        .reset_index()
    )

if "Region" in filtered_df.columns:
    region_summary = (
        filtered_df.groupby("Region")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
        .reset_index()
    )

if "State" in filtered_df.columns:
    state_summary = (
        filtered_df.groupby("State")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .reset_index()
    )

if "City" in filtered_df.columns:
    city_summary = (
        filtered_df.groupby("City")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .reset_index()
    )

if "Segment" in filtered_df.columns:
    segment_summary = (
        filtered_df.groupby("Segment")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
        .reset_index()
    )

if "Ship Mode" in filtered_df.columns:
    ship_summary = (
        filtered_df.groupby("Ship Mode")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
        .reset_index()
    )

if "Discount" in filtered_df.columns and "Profit" in filtered_df.columns:
    discount_data = filtered_df.copy()
    discount_data["Discount Range"] = pd.cut(
        discount_data["Discount"],
        bins=[-0.01, 0, 0.10, 0.20, 0.30, 0.40, 1.00],
        labels=["0%", "1-10%", "11-20%", "21-30%", "31-40%", "40%+"],
    )
    discount_summary = (
        discount_data.groupby("Discount Range", observed=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
        .reset_index()
    )
    scatter_fig = px.scatter(
        filtered_df,
        x="Discount",
        y="Profit",
        size="Sales",
        title="Discount vs Profit",
        hover_data=["Sales", "Quantity"],
    )
    scatter_fig = style_plot(scatter_fig, x_title="Discount", y_title="Profit")
    correlation = filtered_df["Discount"].corr(filtered_df["Profit"])


# ============================================================
# 12. KPI DASHBOARD
# ============================================================

st.subheader("📈 Business KPIs")

kpi_cols = st.columns(4)

with kpi_cols[0]:
    st.metric(
        "💰 Total Sales",
        f"${total_sales:,.2f}",
        help="Total sales generated by the filtered records.",
    )

with kpi_cols[1]:
    st.metric(
        "📈 Total Profit",
        f"${total_profit:,.2f}",
        help="Net profit generated across the selected dataset.",
    )

with kpi_cols[2]:
    st.metric(
        "📦 Quantity Sold",
        f"{int(total_quantity):,}",
        help="Total units sold in the filtered view.",
    )

with kpi_cols[3]:
    st.metric(
        "📊 Profit Margin",
        f"{profit_margin:.2f}%",
        help="Profit as a percentage of total sales.",
    )

kpi_cols = st.columns(4)
with kpi_cols[0]:
    st.metric(
        "🧾 Records",
        f"{total_records:,}",
        help="Number of rows included in the current filter selection.",
    )

with kpi_cols[1]:
    st.metric(
        "💵 Avg Sales / Record",
        f"${average_sales:,.2f}",
        help="Average sales value per record in the filtered dataset.",
    )

with kpi_cols[2]:
    st.metric(
        "🏙️ Cities",
        f"{total_cities:,}",
        help="Distinct cities represented in the filtered data.",
    )

with kpi_cols[3]:
    st.metric(
        "📍 States",
        f"{total_states:,}",
        help="Distinct states represented in the filtered data.",
    )

average_profit_per_record = total_profit / total_records if total_records else 0
profit_margin_status = (
    "🟢 Strong"
    if profit_margin >= 20
    else "🟡 Moderate"
    if profit_margin >= 10
    else "🔴 Needs Attention"
)

health_cols = st.columns([1.5, 2.5])
with health_cols[0]:
    st.subheader("Business Health")
    st.markdown(
        f'<div class="health-card"><strong>{profit_margin_status}</strong><br>'
        f'<span>Current profit margin: {profit_margin:.2f}%</span></div>',
        unsafe_allow_html=True,
    )
with health_cols[1]:
    st.caption("Current profit margin based on the active filters.")
    st.write(f"Profit Margin: **{profit_margin:.2f}%**")
    st.write(f"Average Profit per Record: **${average_profit_per_record:,.2f}**")

# ============================================================
# 13. EXECUTIVE SUMMARY
# ============================================================

st.markdown("---")
st.subheader("Executive Summary")
st.caption("Dynamic decision summary based on the current filter selection.")

summary_category = (
    filtered_df.groupby("Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    if "Category" in filtered_df.columns
    else pd.DataFrame()
)
summary_region = (
    filtered_df.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    if "Region" in filtered_df.columns
    else pd.DataFrame()
)
summary_subcategory = (
    filtered_df.groupby("Sub-Category")["Profit"].sum()
    if "Sub-Category" in filtered_df.columns
    else pd.Series(dtype=float)
)
summary_state = (
    filtered_df.groupby("State")["Profit"].sum()
    if "State" in filtered_df.columns
    else pd.Series(dtype=float)
)

overall_cols = st.columns(5)
overall_metrics = [
    ("Total Sales", f"${total_sales:,.2f}"),
    ("Total Profit", f"${total_profit:,.2f}"),
    ("Quantity Sold", f"{int(total_quantity):,}"),
    ("Profit Margin", f"{profit_margin:.2f}%"),
    ("Number of Records", f"{total_records:,}"),
]
for metric_col, (label, value) in zip(overall_cols, overall_metrics):
    with metric_col:
        st.metric(label, value)

best_cols = st.columns(2)
with best_cols[0]:
    st.markdown("**Best Performers**")
    if not summary_category.empty:
        st.write(f"Highest sales category: **{summary_category['Sales'].idxmax()}**")
        st.write(f"Most profitable category: **{summary_category['Profit'].idxmax()}**")
    if not summary_region.empty:
        st.write(f"Highest sales region: **{summary_region['Sales'].idxmax()}**")
        st.write(f"Most profitable region: **{summary_region['Profit'].idxmax()}**")
    if not summary_subcategory.empty:
        st.write(f"Most profitable sub-category: **{summary_subcategory.idxmax()}**")
    if not summary_state.empty:
        st.write(f"Most profitable state: **{summary_state.idxmax()}**")

with best_cols[1]:
    st.markdown("**Areas Requiring Attention**")
    if not summary_category.empty:
        st.write(f"Lowest profit category: **{summary_category['Profit'].idxmin()}**")
    if not summary_region.empty:
        st.write(f"Lowest profit region: **{summary_region['Profit'].idxmin()}**")
    if not summary_subcategory.empty:
        st.write(f"Lowest profit sub-category: **{summary_subcategory.idxmin()}**")
    if not summary_state.empty:
        st.write(f"Lowest profit state: **{summary_state.idxmin()}**")
    negative_groups = []
    for group_name, group_data in [
        ("segment", filtered_df.groupby("Segment")["Profit"].sum() if "Segment" in filtered_df.columns else pd.Series(dtype=float)),
        ("category", summary_category["Profit"] if not summary_category.empty else pd.Series(dtype=float)),
        ("region", summary_region["Profit"] if not summary_region.empty else pd.Series(dtype=float)),
    ]:
        if (group_data < 0).any():
            negative_groups.append(group_name)
    if negative_groups:
        st.write("Negative total profit exists in the selected " + ", ".join(negative_groups) + ".")
    else:
        st.write("No selected segment, category, or region has negative total profit.")

story = []
if not summary_category.empty:
    story.append(f"{summary_category['Sales'].idxmax()} generates the highest sales among the selected categories.")
if not summary_region.empty:
    story.append(f"{summary_region['Profit'].idxmax()} has the strongest regional profitability.")
if not summary_subcategory.empty and summary_subcategory.min() < 0:
    story.append(f"{summary_subcategory.idxmin()} is loss-making and requires performance review.")
if profit_margin < 10:
    story.append("The selected data has a low profit margin and requires closer profitability management.")
elif total_profit >= 0:
    story.append(f"The filtered business generates ${total_profit:,.2f} profit at a {profit_margin:.2f}% margin.")
st.markdown("**Business Story**")
for statement in story[:5]:
    st.write(f"- {statement}")

recommendations = []
if not summary_category.empty:
    recommendations.append(f"Focus commercial attention on {summary_category['Profit'].idxmax()}, the leading profit category.")
if not summary_region.empty:
    recommendations.append(f"Prioritize strong practices from {summary_region['Profit'].idxmax()} and review {summary_region['Profit'].idxmin()}.")
if not summary_subcategory.empty and summary_subcategory.min() < 0:
    recommendations.append(f"Investigate {summary_subcategory.idxmin()} to identify the drivers of negative profit.")
if not summary_state.empty and summary_state.min() < 0:
    recommendations.append(f"Create a recovery plan for {summary_state.idxmin()}, the lowest-profit state.")
if "Discount" in filtered_df.columns and "Profit" in filtered_df.columns:
    discount_correlation = filtered_df["Discount"].corr(filtered_df["Profit"])
    if pd.notna(discount_correlation) and discount_correlation < 0:
        recommendations.append("Review high-discount transactions because discounting is negatively related to profit.")
    else:
        recommendations.append("Monitor discount levels alongside profit to protect sustainable margins.")
st.markdown("**Recommendations**")
for recommendation in recommendations[:5]:
    st.write(f"- {recommendation}")

takeaway_category = summary_category["Profit"].idxmax() if not summary_category.empty else "the selected categories"
takeaway_region = summary_region["Profit"].idxmax() if not summary_region.empty else "the selected regions"
loss_note = (
    f" Loss-making areas include {summary_subcategory.idxmin()}."
    if not summary_subcategory.empty and summary_subcategory.min() < 0
    else ""
)
st.markdown(
    f'<div class="analyst-takeaway"><strong>Analyst Takeaway</strong><br>'
    f'The filtered dataset produced ${total_sales:,.2f} in sales and ${total_profit:,.2f} in profit '
    f'at a {profit_margin:.2f}% margin. {takeaway_category} and {takeaway_region} are the leading '
    f'profit contributors.{loss_note}</div>',
    unsafe_allow_html=True,
)

# ============================================================
# 13. PERFORMANCE RANKING
# ============================================================

st.markdown("---")
st.subheader("Performance Ranking")
st.caption("Compare filtered business groups by profitability and supporting metrics.")

ranking_dimension = st.selectbox(
    "Choose ranking dimension",
    ["Category", "Sub-Category", "Region", "State"],
    key="performance_ranking_dimension",
)


def add_performance_status(table, profit_column="Profit"):
    """Classify groups relative to the profitability distribution in the table."""
    result = table.copy()
    if result.empty or profit_column not in result.columns:
        result["Performance Status"] = pd.Series(dtype="object")
        return result

    profits = result[profit_column].dropna()
    if profits.empty:
        result["Performance Status"] = "Average Performer"
        return result

    high_threshold = profits.quantile(0.75)
    low_threshold = profits.quantile(0.25)
    result["Performance Status"] = result[profit_column].apply(
        lambda value: (
            "High Performer"
            if value >= high_threshold
            else "Low Performer"
            if value <= low_threshold
            else "Average Performer"
        )
    )
    return result


def add_margin(table):
    result = table.copy()
    result["Profit Margin"] = (
        result["Profit"].div(result["Sales"].where(result["Sales"].ne(0))).mul(100)
        .replace([float("inf"), -float("inf")], 0)
        .fillna(0)
    )
    return result


if filtered_df.empty:
    st.info("No ranking data is available for the selected filters.")
else:
    ranking_table = pd.DataFrame()
    if ranking_dimension == "Category" and "Category" in filtered_df.columns:
        ranking_table = (
            filtered_df.groupby("Category")
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
                Quantity=("Quantity", "sum"),
                **{"Average Discount": ("Discount", "mean")},
            )
            .reset_index()
        )
        ranking_table = add_margin(ranking_table).sort_values("Profit", ascending=False)
        ranking_table.insert(0, "Rank", range(1, len(ranking_table) + 1))
    elif ranking_dimension == "Sub-Category" and "Sub-Category" in filtered_df.columns:
        ranking_table = (
            filtered_df.groupby("Sub-Category")
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
                Quantity=("Quantity", "sum"),
                Discount=("Discount", "mean"),
            )
            .reset_index()
        )
        ranking_table = add_margin(ranking_table).sort_values("Profit", ascending=False)
        ranking_table.insert(0, "Rank", range(1, len(ranking_table) + 1))
    elif ranking_dimension == "Region" and "Region" in filtered_df.columns:
        ranking_table = (
            filtered_df.groupby("Region")
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
            .reset_index()
        )
        ranking_table = add_margin(ranking_table).sort_values("Profit", ascending=False)
        ranking_table.insert(0, "Rank", range(1, len(ranking_table) + 1))
    elif ranking_dimension == "State" and "State" in filtered_df.columns:
        ranking_table = (
            filtered_df.groupby("State")
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
            .reset_index()
        )
        ranking_table = add_margin(ranking_table).sort_values("Profit", ascending=False)
        ranking_table.insert(0, "Rank", range(1, len(ranking_table) + 1))

    if ranking_table.empty:
        st.info(f"No {ranking_dimension.lower()} ranking data is available.")
    elif ranking_dimension == "State":
        ranking_table = add_performance_status(ranking_table)
        st.markdown("**Top 10 states by profit**")
        top_state_table = ranking_table.head(10)
        st.dataframe(
            top_state_table.style.format(
                {"Sales": "${:,.2f}", "Profit": "${:,.2f}", "Profit Margin": "{:.2f}%"}
            ),
            width="stretch",
            hide_index=True,
        )
        st.markdown("**Bottom 10 states by profit**")
        bottom_state_table = ranking_table.sort_values("Profit").head(10)
        st.dataframe(
            bottom_state_table.style.format(
                {"Sales": "${:,.2f}", "Profit": "${:,.2f}", "Profit Margin": "{:.2f}%"}
            ),
            width="stretch",
            hide_index=True,
        )
    else:
        ranking_table = add_performance_status(ranking_table)
        format_rules = {
            "Sales": "${:,.2f}",
            "Profit": "${:,.2f}",
            "Profit Margin": "{:.2f}%",
            "Quantity": "{:,.0f}",
            "Average Discount": "{:.2%}",
            "Discount": "{:.2%}",
        }
        st.dataframe(
            ranking_table.style.format(
                {key: value for key, value in format_rules.items() if key in ranking_table.columns}
            ),
            width="stretch",
            hide_index=True,
        )

st.caption("The ranking is based on profitability within the currently selected filters.")


summary_data = {
    "Metric": [
        "Total Sales",
        "Total Profit",
        "Profit Margin",
        "Quantity Sold",
        "Average Sales per Record",
        "Records",
        "Cities",
        "States",
        "Sub-Categories",
    ],
    "Value": [
        f"${total_sales:,.2f}",
        f"${total_profit:,.2f}",
        f"{profit_margin:.2f}%",
        f"{int(total_quantity):,}",
        f"${average_sales:,.2f}",
        f"{total_records:,}",
        f"{total_cities:,}",
        f"{total_states:,}",
        f"{total_subcategories:,}",
    ],
}
summary_csv_data = pd.DataFrame(summary_data).to_csv(index=False).encode("utf-8")


# ============================================================
# 13. TABS
# ============================================================

overview_tab, category_tab, regional_tab, segment_tab, discount_tab, insights_tab, explorer_tab = st.tabs(
    [
        "Overview",
        "Category Analysis",
        "Regional Analysis",
        "Segment & Shipping",
        "Discount Analysis",
        "Business Insights",
        "Data Explorer",
    ]
)

with overview_tab:
    st.caption("Executive overview of category and regional performance")

    st.subheader("Profitability Analysis")
    if category_summary is not None:
        category_profitability = category_summary.copy()
        category_profitability["Profit Margin"] = (
            category_profitability["Profit"] / category_profitability["Sales"] * 100
        ).replace([float("inf"), -float("inf")], 0).fillna(0)

        profitability_cols = st.columns(5)
        with profitability_cols[0]:
            st.metric("Total Sales", f"${category_profitability['Sales'].sum():,.2f}", help="Total sales generated by the current filtered view.")
        with profitability_cols[1]:
            st.metric("Total Profit", f"${category_profitability['Profit'].sum():,.2f}", help="Total net profit across the selected records.")
        with profitability_cols[2]:
            st.metric("Profit Margin", f"{(category_profitability['Profit'].sum() / category_profitability['Sales'].sum() * 100 if category_profitability['Sales'].sum() else 0):.2f}%", help="Profit divided by sales multiplied by 100.")
        with profitability_cols[3]:
            st.metric("Avg Profit / Record", f"${(category_profitability['Profit'].sum() / total_records if total_records else 0):,.2f}", help="Average profit earned per record in the filtered dataset.")
        with profitability_cols[4]:
            st.metric("Total Quantity", f"{int(total_quantity):,}", help="Total quantity sold in the active filter selection.")

        col1, col2 = st.columns(2)
        with col1:
            sales_profit_long = category_profitability.melt(
                id_vars=["Category", "Quantity"],
                value_vars=["Sales", "Profit"],
                var_name="Metric",
                value_name="Amount",
            )
            sales_vs_profit = px.bar(
                sales_profit_long,
                x="Category",
                y="Amount",
                color="Metric",
                barmode="group",
                hover_data={"Category": True, "Metric": True, "Amount": ":,.2f", "Quantity": True},
                title="Sales vs Profit by Category",
            )
            sales_vs_profit = style_plot(sales_vs_profit, x_title="Category", y_title="Amount ($)")
            st.plotly_chart(sales_vs_profit, width="stretch")

        with col2:
            margin_chart = px.bar(
                category_profitability.sort_values("Profit Margin", ascending=False),
                x="Category",
                y="Profit Margin",
                text_auto=".2f",
                title="Profit Margin by Category",
                hover_data={"Category": True, "Profit Margin": ":,.2f"},
            )
            margin_chart = style_plot(margin_chart, x_title="Category", y_title="Profit Margin (%)")
            st.plotly_chart(margin_chart, width="stretch")

    st.markdown("---")
    st.subheader("Quantity Analysis")
    if "Category" in filtered_df.columns:
        quantity_category = filtered_df.groupby("Category")["Quantity"].sum().reset_index().sort_values("Quantity", ascending=False)
        fig = px.bar(quantity_category, x="Category", y="Quantity", title="Quantity by Category", hover_data={"Category": True, "Quantity": True})
        fig = style_plot(fig, x_title="Category", y_title="Quantity")
        st.plotly_chart(fig, width="stretch", key="regional_sales_by_region")

    if "Region" in filtered_df.columns:
        quantity_region = filtered_df.groupby("Region")["Quantity"].sum().reset_index().sort_values("Quantity", ascending=False)
        fig = px.bar(quantity_region, x="Region", y="Quantity", title="Quantity by Region", hover_data={"Region": True, "Quantity": True})
        fig = style_plot(fig, x_title="Region", y_title="Quantity")
        st.plotly_chart(fig, width="stretch", key="regional_profit_by_region")

    if "Segment" in filtered_df.columns:
        quantity_segment = filtered_df.groupby("Segment")["Quantity"].sum().reset_index().sort_values("Quantity", ascending=False)
        fig = px.bar(quantity_segment, x="Segment", y="Quantity", title="Quantity by Segment", hover_data={"Segment": True, "Quantity": True})
        fig = style_plot(fig, x_title="Segment", y_title="Quantity")
        st.plotly_chart(fig, width="stretch", key="regional_top_states_sales")

    st.markdown("---")
    st.subheader("Top & Bottom Performers")
    if state_summary is not None:
        top_states_sales = state_summary.sort_values("Sales", ascending=False).head(10)
        top_states_profit = state_summary.sort_values("Profit", ascending=False).head(10)
        bottom_states_profit = state_summary.sort_values("Profit", ascending=True).head(10)
        top_cities_sales = city_summary.sort_values("Sales", ascending=False).head(10) if city_summary is not None else None
        top_cities_profit = city_summary.sort_values("Profit", ascending=False).head(10) if city_summary is not None else None
        bottom_cities_profit = city_summary.sort_values("Profit", ascending=True).head(10) if city_summary is not None else None

        cols = st.columns(2)
        with cols[0]:
            fig = px.bar(top_states_sales, x="Sales", y="State", orientation="h", title="Top 10 States by Sales", hover_data={"State": True, "Sales": ":,.2f"})
            fig = style_plot(fig, x_title="Sales ($)", y_title="State")
            st.plotly_chart(fig, width="stretch", key="regional_top_states_profit")
        with cols[1]:
            fig = px.bar(top_states_profit, x="Profit", y="State", orientation="h", title="Top 10 States by Profit", hover_data={"State": True, "Profit": ":,.2f"})
            fig = style_plot(fig, x_title="Profit ($)", y_title="State")
            st.plotly_chart(fig, width="stretch", key="regional_bottom_states_profit")

        fig = px.bar(bottom_states_profit, x="Profit", y="State", orientation="h", title="Bottom 10 States by Profit", hover_data={"State": True, "Profit": ":,.2f"})
        fig = style_plot(fig, x_title="Profit ($)", y_title="State")
        st.plotly_chart(fig, width="stretch", key="regional_top_cities_sales")

        if top_cities_sales is not None:
            cols = st.columns(2)
            with cols[0]:
                fig = px.bar(top_cities_sales, x="Sales", y="City", orientation="h", title="Top 10 Cities by Sales", hover_data={"City": True, "Sales": ":,.2f"})
                fig = style_plot(fig, x_title="Sales ($)", y_title="City")
                st.plotly_chart(fig, width="stretch", key="regional_top_cities_profit")
            with cols[1]:
                fig = px.bar(top_cities_profit, x="Profit", y="City", orientation="h", title="Top 10 Cities by Profit", hover_data={"City": True, "Profit": ":,.2f"})
                fig = style_plot(fig, x_title="Profit ($)", y_title="City")
                st.plotly_chart(fig, width="stretch", key="category_tab_sales")

            fig = px.bar(bottom_cities_profit, x="Profit", y="City", orientation="h", title="Bottom 10 Cities by Profit", hover_data={"City": True, "Profit": ":,.2f"})
            fig = style_plot(fig, x_title="Profit ($)", y_title="City")
            st.plotly_chart(fig, width="stretch", key="category_tab_profit")

    if subcategory_summary is not None:
        sub_top_profit = subcategory_summary.sort_values("Profit", ascending=False).head(10)
        sub_bottom_profit = subcategory_summary.sort_values("Profit", ascending=True).head(10)
        cols = st.columns(2)
        with cols[0]:
            fig = px.bar(sub_top_profit, x="Profit", y="Sub-Category", orientation="h", title="Top 10 Sub-Categories by Profit", hover_data={"Sub-Category": True, "Profit": ":,.2f"})
            fig = style_plot(fig, x_title="Profit ($)", y_title="Sub-Category")
            st.plotly_chart(fig, width="stretch", key="category_tab_subcategory_sales")
        with cols[1]:
            fig = px.bar(sub_bottom_profit, x="Profit", y="Sub-Category", orientation="h", title="Bottom 10 Sub-Categories by Profit", hover_data={"Sub-Category": True, "Profit": ":,.2f"})
            fig = style_plot(fig, x_title="Profit ($)", y_title="Sub-Category")
            st.plotly_chart(fig, width="stretch", key="category_tab_subcategory_profit")

    if category_summary is not None:
        category_profitability = category_summary.copy()
        category_profitability["Profit Margin"] = ((category_profitability["Profit"] / category_profitability["Sales"]) * 100).replace([float("inf"), -float("inf")], 0).fillna(0)

    if region_summary is not None:
        region_profitability = region_summary.copy()
        region_profitability["Profit Margin"] = ((region_profitability["Profit"] / region_profitability["Sales"]) * 100).replace([float("inf"), -float("inf")], 0).fillna(0)

    if category_summary is not None:
        st.markdown("---")
        st.subheader("📊 Profitability Table")
        profitability_table = category_summary.copy()
        profitability_table["Profit Margin"] = (
            (profitability_table["Profit"] / profitability_table["Sales"]) * 100
        ).replace([float("inf"), -float("inf")], 0).fillna(0)
        profitability_table = profitability_table[["Category", "Sales", "Profit", "Profit Margin", "Quantity"]].sort_values("Profit", ascending=False)
        st.dataframe(profitability_table, width="stretch", hide_index=True)

    if region_summary is not None:
        st.markdown("---")
        st.subheader("📍 Regional Profitability Table")
        region_profitability_table = region_summary.copy()
        region_profitability_table["Profit Margin"] = (
            (region_profitability_table["Profit"] / region_profitability_table["Sales"]) * 100
        ).replace([float("inf"), -float("inf")], 0).fillna(0)
        region_profitability_table = region_profitability_table[["Region", "Sales", "Profit", "Profit Margin"]].sort_values("Profit", ascending=False)
        st.dataframe(region_profitability_table, width="stretch", hide_index=True)

    if category_summary is not None:
        st.markdown("---")
        st.subheader("Business Summary")
        summary_data = {
            "Metric": [
                "Total Sales",
                "Total Profit",
                "Profit Margin",
                "Quantity Sold",
                "Records",
                "Cities",
                "States",
                "Sub-Categories",
            ],
            "Value": [
                f"${total_sales:,.2f}",
                f"${total_profit:,.2f}",
                f"{profit_margin:.2f}%",
                f"{int(total_quantity):,}",
                f"{total_records:,}",
                f"{total_cities:,}",
                f"{total_states:,}",
                f"{total_subcategories:,}",
            ],
        }
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, width="stretch", hide_index=True)

    if category_summary is not None:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                category_summary.sort_values("Sales", ascending=False),
                x="Category",
                y="Sales",
                text_auto=".2s",
                title="Category Sales Overview",
                hover_data={"Category": True, "Sales": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Category", y_title="Sales ($)")
            st.plotly_chart(fig, width="stretch")

        with col2:
            fig = px.bar(
                category_summary.sort_values("Profit", ascending=False),
                x="Category",
                y="Profit",
                text_auto=".2s",
                title="Category Profit Overview",
                hover_data={"Category": True, "Profit": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Category", y_title="Profit ($)")
            st.plotly_chart(fig, width="stretch")

    if region_summary is not None:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                region_summary.sort_values("Sales", ascending=False),
                x="Region",
                y="Sales",
                text_auto=".2s",
                title="Regional Sales Overview",
                hover_data={"Region": True, "Sales": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Region", y_title="Sales ($)")
            st.plotly_chart(fig, width="stretch")

        with col2:
            fig = px.bar(
                region_summary.sort_values("Profit", ascending=False),
                x="Region",
                y="Profit",
                text_auto=".2s",
                title="Regional Profit Overview",
                hover_data={"Region": True, "Profit": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Region", y_title="Profit ($)")
            st.plotly_chart(fig, width="stretch")

    st.markdown("---")
    st.subheader("📋 Business Summary")
    summary_data = {
        "Metric": [
            "Total Sales",
            "Total Profit",
            "Profit Margin",
            "Quantity Sold",
            "Records",
            "Cities",
            "States",
            "Sub-Categories",
        ],
        "Value": [
            f"${total_sales:,.2f}",
            f"${total_profit:,.2f}",
            f"{profit_margin:.2f}%",
            f"{int(total_quantity):,}",
            f"{total_records:,}",
            f"{total_cities:,}",
            f"{total_states:,}",
            f"{total_subcategories:,}",
        ],
    }
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, width="stretch", hide_index=True)

with category_tab:
    st.subheader("📦 Category Performance")
    if category_summary is not None:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                category_summary.sort_values("Sales", ascending=False),
                x="Category",
                y="Sales",
                text_auto=".2s",
                title="Sales by Category",
                hover_data={"Category": True, "Sales": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Category", y_title="Sales ($)")
            st.plotly_chart(fig, width="stretch")

        with col2:
            fig = px.bar(
                category_summary.sort_values("Profit", ascending=False),
                x="Category",
                y="Profit",
                text_auto=".2s",
                title="Profit by Category",
                hover_data={"Category": True, "Profit": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Category", y_title="Profit ($)")
            st.plotly_chart(fig, width="stretch")

    st.markdown("---")
    st.subheader("📦 Sub-Category Performance")
    if subcategory_summary is not None:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                subcategory_summary.sort_values("Sales", ascending=False),
                x="Sub-Category",
                y="Sales",
                text_auto=".2s",
                title="Sales by Sub-Category",
                hover_data={"Sub-Category": True, "Sales": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Sub-Category", y_title="Sales ($)")
            st.plotly_chart(fig, width="stretch")

        with col2:
            fig = px.bar(
                subcategory_summary.sort_values("Profit", ascending=False),
                x="Sub-Category",
                y="Profit",
                text_auto=".2s",
                title="Profit by Sub-Category",
                hover_data={"Sub-Category": True, "Profit": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Sub-Category", y_title="Profit ($)")
            st.plotly_chart(fig, width="stretch")

with regional_tab:
    st.subheader("🌎 Region Performance")
    if region_summary is not None:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                region_summary.sort_values("Sales", ascending=False),
                x="Region",
                y="Sales",
                text_auto=".2s",
                title="Sales by Region",
                hover_data={"Region": True, "Sales": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Region", y_title="Sales ($)")
            st.plotly_chart(fig, width="stretch")

        with col2:
            fig = px.bar(
                region_summary.sort_values("Profit", ascending=False),
                x="Region",
                y="Profit",
                text_auto=".2s",
                title="Profit by Region",
                hover_data={"Region": True, "Profit": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Region", y_title="Profit ($)")
            st.plotly_chart(fig, width="stretch")

    st.markdown("---")
    st.subheader("📍 State Performance")
    if state_summary is not None:
        top_sales_states = state_summary.sort_values("Sales", ascending=False).head(10)
        top_profit_states = state_summary.sort_values("Profit", ascending=False).head(10)
        bottom_profit_states = state_summary.sort_values("Profit", ascending=True).head(10)

        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                top_sales_states,
                x="Sales",
                y="State",
                orientation="h",
                title="Top 10 States by Sales",
                hover_data={"State": True, "Sales": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Sales ($)", y_title="State")
            st.plotly_chart(fig, width="stretch")

        with col2:
            fig = px.bar(
                top_profit_states,
                x="Profit",
                y="State",
                orientation="h",
                title="Top 10 States by Profit",
                hover_data={"State": True, "Profit": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Profit ($)", y_title="State")
            st.plotly_chart(fig, width="stretch")

        fig = px.bar(
            bottom_profit_states,
            x="Profit",
            y="State",
            orientation="h",
            title="Bottom 10 States by Profit",
            hover_data={"State": True, "Profit": ":,.2f"},
        )
        fig = style_plot(fig, x_title="Profit ($)", y_title="State")
        st.plotly_chart(fig, width="stretch")

    st.markdown("---")
    st.subheader("🏙️ City Performance")
    if city_summary is not None:
        top_cities_sales = city_summary.sort_values("Sales", ascending=False).head(10)
        top_cities_profit = city_summary.sort_values("Profit", ascending=False).head(10)

        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                top_cities_sales,
                x="Sales",
                y="City",
                orientation="h",
                title="Top 10 Cities by Sales",
                hover_data={"City": True, "Sales": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Sales ($)", y_title="City")
            st.plotly_chart(fig, width="stretch")

        with col2:
            fig = px.bar(
                top_cities_profit,
                x="Profit",
                y="City",
                orientation="h",
                title="Top 10 Cities by Profit",
                hover_data={"City": True, "Profit": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Profit ($)", y_title="City")
            st.plotly_chart(fig, width="stretch")

with segment_tab:
    st.subheader("👥 Customer Segment Performance")
    if segment_summary is not None:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(
                segment_summary,
                names="Segment",
                values="Sales",
                title="Sales Distribution by Segment",
                hover_data={"Segment": True, "Sales": ":,.2f"},
            )
            fig = style_plot(fig)
            st.plotly_chart(fig, width="stretch")

        with col2:
            fig = px.bar(
                segment_summary.sort_values("Profit", ascending=False),
                x="Segment",
                y="Profit",
                text_auto=".2s",
                title="Profit by Segment",
                hover_data={"Segment": True, "Profit": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Segment", y_title="Profit ($)")
            st.plotly_chart(fig, width="stretch")

    st.markdown("---")
    st.subheader("🚚 Ship Mode Performance")
    if ship_summary is not None:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                ship_summary.sort_values("Sales", ascending=False),
                x="Ship Mode",
                y="Sales",
                text_auto=".2s",
                title="Sales by Ship Mode",
                hover_data={"Ship Mode": True, "Sales": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Ship Mode", y_title="Sales ($)")
            st.plotly_chart(fig, width="stretch")

        with col2:
            fig = px.bar(
                ship_summary.sort_values("Profit", ascending=False),
                x="Ship Mode",
                y="Profit",
                text_auto=".2s",
                title="Profit by Ship Mode",
                hover_data={"Ship Mode": True, "Profit": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Ship Mode", y_title="Profit ($)")
            st.plotly_chart(fig, width="stretch")

    st.markdown("---")
    st.subheader("Segment & Business Performance Analysis")
    st.caption("Compare segment contribution, profitability, and operating mix using the active filters.")

    if filtered_df.empty or "Segment" not in filtered_df.columns:
        st.info("No segment data is available for the selected filters.")
    else:
        segment_data = filtered_df.dropna(subset=["Segment"]).copy()
        required_segment_columns = {"Sales", "Profit", "Quantity", "Discount"}
        if segment_data.empty or not required_segment_columns.issubset(segment_data.columns):
            st.info("Segment analysis requires available Sales, Profit, Quantity, and Discount values.")
        else:
            segment_performance = (
                segment_data.groupby("Segment")
                .agg(
                    Sales=("Sales", "sum"),
                    Profit=("Profit", "sum"),
                    Quantity=("Quantity", "sum"),
                    **{"Average Discount": ("Discount", "mean"), "Number of Records": ("Profit", "size")},
                )
                .reset_index()
            )
            segment_performance["Profit Margin"] = (
                segment_performance["Profit"].div(
                    segment_performance["Sales"].where(segment_performance["Sales"].ne(0))
                ).mul(100).replace([float("inf"), -float("inf")], 0).fillna(0)
            )
            segment_performance["Average Sales per Record"] = (
                segment_performance["Sales"].div(segment_performance["Number of Records"].where(segment_performance["Number of Records"].ne(0)))
                .replace([float("inf"), -float("inf")], 0).fillna(0)
            )
            segment_performance["Average Profit per Record"] = (
                segment_performance["Profit"].div(segment_performance["Number of Records"].where(segment_performance["Number of Records"].ne(0)))
                .replace([float("inf"), -float("inf")], 0).fillna(0)
            )
            segment_performance = segment_performance.sort_values("Profit", ascending=False)
            st.markdown("**Segment Performance**")
            st.dataframe(
                segment_performance.style.format(
                    {
                        "Sales": "${:,.2f}", "Profit": "${:,.2f}", "Quantity": "{:,.0f}",
                        "Average Discount": "{:.2%}", "Profit Margin": "{:.2f}%",
                        "Average Sales per Record": "${:,.2f}", "Average Profit per Record": "${:,.2f}",
                        "Number of Records": "{:,.0f}",
                    }
                ),
                width="stretch",
                hide_index=True,
            )

            segment_chart_cols = st.columns(2)
            with segment_chart_cols[0]:
                sales_segment_fig = px.bar(
                    segment_performance.sort_values("Sales", ascending=False),
                    x="Segment", y="Sales", text_auto=".2s",
                    title="Sales by Segment",
                    hover_data={"Segment": True, "Sales": ":,.2f", "Number of Records": True},
                )
                sales_segment_fig = style_plot(sales_segment_fig, x_title="Segment", y_title="Sales ($)")
                st.plotly_chart(sales_segment_fig, width="stretch")
            with segment_chart_cols[1]:
                profit_segment_fig = px.bar(
                    segment_performance.sort_values("Profit", ascending=False),
                    x="Segment", y="Profit", text_auto=".2s",
                    color="Profit",
                    color_continuous_scale=["#dc2626", "#f59e0b", "#16a34a"],
                    title="Profit by Segment",
                    hover_data={"Segment": True, "Profit": ":,.2f", "Profit Margin": ":.2f"},
                )
                profit_segment_fig = style_plot(profit_segment_fig, x_title="Segment", y_title="Profit ($)")
                st.plotly_chart(profit_segment_fig, width="stretch")

            mix_cols = st.columns(2)
            with mix_cols[0]:
                segment_mix_fig = px.pie(
                    segment_performance, names="Segment", values="Sales", hole=0.55,
                    title="Segment Sales Mix",
                    hover_data={"Sales": ":,.2f"},
                )
                segment_mix_fig = style_plot(segment_mix_fig)
                st.plotly_chart(segment_mix_fig, width="stretch")
            with mix_cols[1]:
                best_segment_metrics = {
                    "Highest Sales Segment": segment_performance.loc[segment_performance["Sales"].idxmax(), "Segment"],
                    "Most Profitable Segment": segment_performance.loc[segment_performance["Profit"].idxmax(), "Segment"],
                    "Highest Quantity Segment": segment_performance.loc[segment_performance["Quantity"].idxmax(), "Segment"],
                    "Best Profit Margin Segment": segment_performance.loc[segment_performance["Profit Margin"].idxmax(), "Segment"],
                }
                st.markdown("**Best Segment**")
                for label, value in best_segment_metrics.items():
                    st.write(f"{label}: **{value}**")
                weakest_segment = segment_performance.iloc[-1]
                if weakest_segment["Profit"] < 0:
                    st.warning(f"{weakest_segment['Segment']} has negative total profit and requires attention.")
                elif (segment_performance["Profit"] < 0).any():
                    st.warning("At least one segment has negative total profit and requires attention.")
                else:
                    st.success("All selected segments are profitable.")

            if {"Category", "Segment"}.issubset(segment_data.columns):
                segment_category = (
                    segment_data.groupby(["Segment", "Category"])
                    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
                    .reset_index()
                )
                segment_category["Profit Margin"] = (
                    segment_category["Profit"].div(
                        segment_category["Sales"].where(segment_category["Sales"].ne(0))
                    ).mul(100).replace([float("inf"), -float("inf")], 0).fillna(0)
                )
                st.markdown("**Segment × Category Analysis**")
                segment_category_fig = px.bar(
                    segment_category, x="Segment", y="Profit", color="Category",
                    barmode="group", title="Profit by Segment and Category",
                    hover_data={"Segment": True, "Category": True, "Profit": ":,.2f", "Profit Margin": ":.2f"},
                )
                segment_category_fig = style_plot(segment_category_fig, x_title="Segment", y_title="Profit ($)")
                st.plotly_chart(segment_category_fig, width="stretch")

            if "Region" in segment_data.columns:
                segment_region = (
                    segment_data.groupby(["Segment", "Region"])
                    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum"))
                    .reset_index()
                )
                segment_region["Profit Margin"] = (
                    segment_region["Profit"].div(
                        segment_region["Sales"].where(segment_region["Sales"].ne(0))
                    ).mul(100).replace([float("inf"), -float("inf")], 0).fillna(0)
                )
                st.markdown("**Segment × Region Analysis**")
                st.dataframe(
                    segment_region.sort_values("Profit", ascending=False).style.format(
                        {"Sales": "${:,.2f}", "Profit": "${:,.2f}", "Quantity": "{:,.0f}", "Profit Margin": "{:.2f}%"}
                    ),
                    width="stretch",
                    hide_index=True,
                )

            st.markdown("**Dynamic Segment Insights & Recommendations**")
            segment_insights = [
                f"{best_segment_metrics['Highest Sales Segment']} contributes the highest sales among selected segments.",
                f"{best_segment_metrics['Most Profitable Segment']} is the most profitable segment.",
                f"{best_segment_metrics['Best Profit Margin Segment']} has the strongest profit margin.",
            ]
            if (segment_performance["Profit"] < 0).any():
                segment_insights.append("A selected segment has negative profit and should be investigated.")
            for insight in segment_insights[:5]:
                st.write(f"- {insight}")

            segment_recommendations = [
                f"Protect the margin profile of {best_segment_metrics['Most Profitable Segment']}.",
                f"Use {best_segment_metrics['Highest Sales Segment']} as a benchmark for sales execution.",
            ]
            if weakest_segment["Profit"] < 0:
                segment_recommendations.append(f"Investigate loss drivers in {weakest_segment['Segment']}.")
            if segment_performance["Average Discount"].corr(segment_performance["Profit Margin"]) < 0:
                segment_recommendations.append("Review discount levels where segment profitability is weaker.")
            for recommendation in segment_recommendations[:5]:
                st.write(f"- {recommendation}")

with explorer_tab:
    st.subheader("Data Explorer")
    explorer_cols = st.columns(8)
    with explorer_cols[0]:
        st.metric("Filtered Records", f"{len(filtered_df):,}")
    with explorer_cols[1]:
        st.metric("Total Columns", f"{len(filtered_df.columns):,}")
    with explorer_cols[2]:
        st.metric("Missing Values", f"{filtered_df.isna().sum().sum():,}")
    with explorer_cols[3]:
        st.metric("Duplicate Rows", f"{filtered_df.duplicated().sum():,}")
    with explorer_cols[4]:
        st.metric("Unique Cities", f"{filtered_df['City'].nunique() if 'City' in filtered_df else 0:,}")
    with explorer_cols[5]:
        st.metric("Unique States", f"{filtered_df['State'].nunique() if 'State' in filtered_df else 0:,}")
    with explorer_cols[6]:
        st.metric("Unique Categories", f"{filtered_df['Category'].nunique() if 'Category' in filtered_df else 0:,}")
    with explorer_cols[7]:
        st.metric("Unique Sub-Categories", f"{filtered_df['Sub-Category'].nunique() if 'Sub-Category' in filtered_df else 0:,}")

    search_text = st.text_input("Search dataset", placeholder="Search across all filtered columns...")
    numeric_sort_options = [
        column for column in ["Sales", "Quantity", "Discount", "Profit"]
        if column in filtered_df.columns
    ]
    explorer_controls = st.columns([2.5, 1.5, 1])
    with explorer_controls[0]:
        selected_columns = st.multiselect(
            "Columns to display",
            options=filtered_df.columns.tolist(),
            default=filtered_df.columns.tolist(),
            key="explorer_columns",
        )
    with explorer_controls[1]:
        sort_column = st.selectbox(
            "Sort by numeric column",
            ["None"] + numeric_sort_options,
            key="explorer_sort_column",
        )
    with explorer_controls[2]:
        sort_direction = st.selectbox(
            "Sort direction",
            ["Descending", "Ascending"],
            key="explorer_sort_direction",
        )

    search_results = filtered_df
    if search_text.strip():
        search_mask = filtered_df.astype(str).apply(
            lambda column: column.str.contains(search_text.strip(), case=False, na=False, regex=False)
        ).any(axis=1)
        search_results = filtered_df[search_mask]

    if search_results.empty:
        st.warning("No records found for your search.")
    else:
        if sort_column != "None":
            search_results = search_results.sort_values(
                sort_column, ascending=sort_direction == "Ascending"
            )
        display_columns = selected_columns or filtered_df.columns.tolist()
        st.caption(f"Showing {len(search_results):,} matching record(s)")
        st.dataframe(
            search_results[display_columns],
            width="stretch",
            height=500,
            hide_index=True,
        )

    st.download_button(
        "Download Filtered Dataset",
        data=search_results.to_csv(index=False).encode("utf-8"),
        file_name="filtered_retail_business_data.csv",
        mime="text/csv",
        key="explorer_filtered_download",
    )
    st.subheader("Data Quality Report")
    quality_report = pd.DataFrame(
        {
            "Column Name": filtered_df.columns,
            "Data Type": filtered_df.dtypes.astype(str).values,
            "Missing Values": filtered_df.isna().sum().values,
            "Missing Percentage": (filtered_df.isna().mean() * 100).round(2).values,
            "Unique Values": filtered_df.nunique(dropna=True).values,
        }
    )
    with st.expander("View Data Quality Report", expanded=False):
        st.dataframe(quality_report, width="stretch", hide_index=True)
    st.subheader("Export Report")
    st.download_button(
        "Download Business Summary CSV",
        data=summary_csv_data,
        file_name="business_summary.csv",
        mime="text/csv",
        key="explorer_summary_download",
    )

with discount_tab:
    st.subheader("Profitability & Discount Analysis")
    st.caption("Profitability and discount behavior for the currently filtered records.")

    overview_cols = st.columns(5)
    profitability_metrics = [
        ("Total Sales", f"${total_sales:,.2f}"),
        ("Total Profit", f"${total_profit:,.2f}"),
        ("Profit Margin", f"{profit_margin:.2f}%"),
        ("Average Discount", f"{filtered_df['Discount'].mean():.2%}" if "Discount" in filtered_df.columns else "0.00%"),
        ("Quantity Sold", f"{int(total_quantity):,}"),
    ]
    for metric_col, (label, value) in zip(overview_cols, profitability_metrics):
        with metric_col:
            st.metric(label, value)

    if filtered_df.empty:
        st.info("No profitability or discount analysis is available for the selected filters.")
    else:
        st.markdown("**Discount vs Profit Analysis**")
        scatter_columns = [
            column for column in ["Category", "Sub-Category", "Sales", "Discount", "Profit", "Region"]
            if column in filtered_df.columns
        ]
        if {"Discount", "Profit"}.issubset(filtered_df.columns):
            discount_scatter = px.scatter(
                filtered_df,
                x="Discount",
                y="Profit",
                color="Category" if "Category" in filtered_df.columns else None,
                hover_data=scatter_columns,
                size="Sales" if "Sales" in filtered_df.columns else None,
                title="Discount vs Profit",
            )
            discount_scatter = style_plot(discount_scatter, x_title="Discount", y_title="Profit ($)")
            st.plotly_chart(discount_scatter, width="stretch")

        if "Discount" in filtered_df.columns and "Profit" in filtered_df.columns:
            range_analysis = filtered_df.copy()
            range_analysis["Discount Range"] = pd.cut(
                range_analysis["Discount"],
                bins=[-0.01, 0, 0.10, 0.20, 0.30, 0.40, 1.00],
                labels=["0%", "1-10%", "11-20%", "21-30%", "31-40%", "40%+"],
            )
            range_table = (
                range_analysis.groupby("Discount Range", observed=False)
                .agg(
                    Sales=("Sales", "sum"),
                    Profit=("Profit", "sum"),
                    Quantity=("Quantity", "sum"),
                    Records=("Profit", "size"),
                )
                .reset_index()
            )
            range_table["Profit Margin"] = (
                range_table["Profit"].div(range_table["Sales"].where(range_table["Sales"].ne(0))).mul(100)
                .replace([float("inf"), -float("inf")], 0)
                .fillna(0)
            )
            st.markdown("**Discount Range Analysis**")
            st.dataframe(
                range_table[["Discount Range", "Sales", "Profit", "Quantity", "Profit Margin", "Records"]].style.format(
                    {"Sales": "${:,.2f}", "Profit": "${:,.2f}", "Quantity": "{:,.0f}", "Profit Margin": "{:.2f}%"}
                ),
                width="stretch",
                hide_index=True,
            )

            average_range_profit = (
                range_analysis.groupby("Discount Range", observed=False)["Profit"].mean().dropna()
            )
            if len(average_range_profit) >= 2:
                low_discount_profit = average_range_profit.iloc[0]
                high_discount_profit = average_range_profit.iloc[-1]
                if high_discount_profit < low_discount_profit or high_discount_profit < 0:
                    st.warning("High-discount transactions show weak or negative profitability and should be reviewed.")
                else:
                    st.success("Higher discount ranges are not currently showing weaker average profitability.")

        if "Category" in filtered_df.columns and {"Discount", "Sales", "Profit"}.issubset(filtered_df.columns):
            category_discount_profit = filtered_df.groupby("Category").agg(
                Average_Discount=("Discount", "mean"),
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
            ).reset_index()
            category_discount_profit["Profit Margin"] = (
                category_discount_profit["Profit"].div(category_discount_profit["Sales"].where(category_discount_profit["Sales"].ne(0))).mul(100)
                .replace([float("inf"), -float("inf")], 0).fillna(0)
            )
            category_chart_data = category_discount_profit.melt(
                id_vars="Category",
                value_vars=["Average_Discount", "Profit Margin"],
                var_name="Metric",
                value_name="Value",
            )
            category_chart_data["Metric"] = category_chart_data["Metric"].replace(
                {"Average_Discount": "Average Discount (%)"}
            )
            category_chart = px.bar(
                category_chart_data,
                x="Category",
                y="Value",
                color="Metric",
                barmode="group",
                title="Average Discount vs Profit Margin by Category",
                hover_data={"Value": ":.2f"},
            )
            category_chart = style_plot(category_chart, x_title="Category", y_title="Percentage")
            st.plotly_chart(category_chart, width="stretch")

        if "Sub-Category" in filtered_df.columns and {"Sales", "Profit", "Discount"}.issubset(filtered_df.columns):
            subcategory_profitability = filtered_df.groupby("Sub-Category").agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
                Average_Discount=("Discount", "mean"),
            ).reset_index()
            subcategory_profitability["Profit Margin"] = (
                subcategory_profitability["Profit"].div(subcategory_profitability["Sales"].where(subcategory_profitability["Sales"].ne(0))).mul(100)
                .replace([float("inf"), -float("inf")], 0).fillna(0)
            )
            subcategory_profitability = subcategory_profitability.sort_values("Profit", ascending=False)
            st.markdown("**Sub-Category Profitability**")
            st.dataframe(
                subcategory_profitability.style.format(
                    {"Sales": "${:,.2f}", "Profit": "${:,.2f}", "Average_Discount": "{:.2%}", "Profit Margin": "{:.2f}%"}
                ).highlight_min(subset=["Profit"], color="#fee2e2"),
                width="stretch",
                hide_index=True,
            )

        loss_records = filtered_df[filtered_df["Profit"] < 0] if "Profit" in filtered_df.columns else pd.DataFrame()
        st.markdown("**Loss-Making Analysis**")
        loss_cols = st.columns(2)
        with loss_cols[0]:
            st.metric("Loss-Making Records", f"{len(loss_records):,}")
        with loss_cols[1]:
            st.metric("Total Loss", f"${abs(loss_records['Profit'].sum()):,.2f}" if not loss_records.empty else "$0.00")
        if loss_records.empty:
            st.success("No loss-making records are present in the selected data.")
        else:
            loss_groups = [
                ("Categories", "Category"),
                ("Sub-Categories", "Sub-Category"),
                ("States", "State"),
            ]
            for label, column in loss_groups:
                if column in loss_records.columns:
                    loss_values = loss_records.groupby(column)["Profit"].sum().sort_values()
                    loss_names = loss_values[loss_values < 0].index.astype(str).tolist()
                    st.write(f"{label} with losses: **{', '.join(loss_names)}**")

        st.markdown("**Business Insights & Recommendations**")
        discount_profit_correlation = (
            filtered_df["Discount"].corr(filtered_df["Profit"])
            if {"Discount", "Profit"}.issubset(filtered_df.columns) else float("nan")
        )
        analysis_insights = []
        if pd.notna(discount_profit_correlation):
            relationship = "negative" if discount_profit_correlation < 0 else "positive"
            analysis_insights.append(
                f"Discount has a {relationship} relationship with profit (correlation: {discount_profit_correlation:.3f})."
            )
        if loss_records.empty:
            analysis_insights.append("The selected data contains no loss-making records.")
        else:
            analysis_insights.append(f"{len(loss_records):,} records generate negative profit and need review.")
        if "Category" in filtered_df.columns:
            best_category = filtered_df.groupby("Category")["Profit"].sum().idxmax()
            analysis_insights.append(f"{best_category} is the leading category by total profit.")
        for insight in analysis_insights[:5]:
            st.write(f"- {insight}")

        recommendations = []
        if pd.notna(discount_profit_correlation) and discount_profit_correlation < 0:
            recommendations.append("Review excessive discounting where it is associated with weaker profitability.")
        if not loss_records.empty and "Sub-Category" in loss_records.columns:
            worst_subcategory = loss_records.groupby("Sub-Category")["Profit"].sum().idxmin()
            recommendations.append(f"Investigate {worst_subcategory}, which contributes the largest sub-category loss.")
        if "Category" in filtered_df.columns:
            best_category = filtered_df.groupby("Category")["Profit"].sum().idxmax()
            recommendations.append(f"Protect margins in {best_category}, the strongest profit contributor.")
        if not loss_records.empty and "State" in loss_records.columns:
            worst_state = loss_records.groupby("State")["Profit"].sum().idxmin()
            recommendations.append(f"Revisit pricing and discount strategy in {worst_state}.")
        for recommendation in recommendations[:5]:
            st.write(f"- {recommendation}")

    st.markdown("---")
    st.subheader("📉 Discount & Profit Analysis")
    if "Discount" in filtered_df.columns:
        avg_discount = filtered_df["Discount"].mean() if not filtered_df.empty else 0
        max_discount = filtered_df["Discount"].max() if not filtered_df.empty else 0
        min_discount = filtered_df["Discount"].min() if not filtered_df.empty else 0
        st.caption("Discount insights for the active filter set")
        disc_cols = st.columns(4)
        with disc_cols[0]:
            st.metric("Average Discount", f"{avg_discount:.2%}", help="Average discount across filtered records.")
        with disc_cols[1]:
            st.metric("Maximum Discount", f"{max_discount:.2%}", help="Largest discount present in the active data.")
        with disc_cols[2]:
            st.metric("Minimum Discount", f"{min_discount:.2%}", help="Smallest discount present in the active data.")
        with disc_cols[3]:
            st.metric("Profit Margin", f"{profit_margin:.2f}%", help="Current overall profit margin for the selected data.")

    if discount_summary is not None:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                discount_summary,
                x="Discount Range",
                y="Sales",
                text_auto=".2s",
                title="Sales by Discount Range",
                hover_data={"Discount Range": True, "Sales": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Discount Range", y_title="Sales ($)")
            st.plotly_chart(fig, width="stretch")

        with col2:
            fig = px.bar(
                discount_summary,
                x="Discount Range",
                y="Profit",
                text_auto=".2s",
                title="Profit by Discount Range",
                hover_data={"Discount Range": True, "Profit": ":,.2f"},
            )
            fig = style_plot(fig, x_title="Discount Range", y_title="Profit ($)")
            st.plotly_chart(fig, width="stretch")

        if scatter_fig is not None:
            st.plotly_chart(scatter_fig, width="stretch")

        if pd.notna(correlation):
            if correlation < 0:
                st.info(
                    f"📌 Discount and profit have a negative correlation of **{correlation:.3f}**."
                )
            elif correlation > 0:
                st.info(
                    f"📌 Discount and profit have a positive correlation of **{correlation:.3f}**."
                )
            else:
                st.info("📌 No meaningful linear relationship was detected between discount and profit.")

    if "Discount" in filtered_df.columns:
        range_profit = filtered_df.copy()
        range_profit["Discount Range"] = pd.cut(
            range_profit["Discount"],
            bins=[-0.01, 0, 0.10, 0.20, 0.30, 0.40, 1.00],
            labels=["0%", "1-10%", "11-20%", "21-30%", "31-40%", "40%+"],
        )
        avg_profit_by_range = (
            range_profit.groupby("Discount Range", observed=False)["Profit"].mean().reset_index().rename(columns={"Profit": "Average Profit"})
        )
        avg_profit_by_range["Average Profit"] = avg_profit_by_range["Average Profit"].fillna(0)

        st.markdown("---")
        st.subheader("📊 Average Profit by Discount Range")
        profit_by_range_fig = px.bar(
            avg_profit_by_range,
            x="Discount Range",
            y="Average Profit",
            text_auto=".2s",
            title="Average Profit by Discount Range",
            hover_data={"Discount Range": True, "Average Profit": ":,.2f"},
        )
        profit_by_range_fig = style_plot(profit_by_range_fig, x_title="Discount Range", y_title="Average Profit ($)")
        st.plotly_chart(profit_by_range_fig, width="stretch")

        if not avg_profit_by_range.empty:
            highest_profit_range = avg_profit_by_range.sort_values("Average Profit", ascending=False).iloc[0]
            lowest_profit_range = avg_profit_by_range.sort_values("Average Profit", ascending=True).iloc[0]
            st.info(
                f"📌 Highest profit range: **{highest_profit_range['Discount Range']}** with average profit of **${highest_profit_range['Average Profit']:,.2f}**."
            )
            st.info(
                f"📌 Lowest profit range: **{lowest_profit_range['Discount Range']}** with average profit of **${lowest_profit_range['Average Profit']:,.2f}**."
            )

with insights_tab:
    st.subheader("💡 Key Business Insights")
    if "Category" in filtered_df.columns:
        category_profit = filtered_df.groupby("Category")["Profit"].sum()
        category_sales = filtered_df.groupby("Category")["Sales"].sum()
        if not category_profit.empty:
            st.write(f"🔹 **{category_profit.idxmax()} is the highest-profit category.**")
        if not category_sales.empty:
            st.write(f"🔹 **{category_sales.idxmax()} leads category sales.**")

    if "Region" in filtered_df.columns:
        region_profit = filtered_df.groupby("Region")["Profit"].sum()
        if not region_profit.empty:
            st.write(f"🔹 **{region_profit.idxmax()} has the strongest regional profitability.**")
            st.write(f"🔹 **{region_profit.idxmin()} has the weakest regional profitability.**")

    if "Sub-Category" in filtered_df.columns:
        subcategory_profit = filtered_df.groupby("Sub-Category")["Profit"].sum()
        if not subcategory_profit.empty:
            st.write(f"🔹 **{subcategory_profit.idxmax()} is the most profitable sub-category.**")
            st.write(f"🔹 **{subcategory_profit.idxmin()} is the lowest-profit sub-category.**")

    if "State" in filtered_df.columns:
        state_summary_insights = filtered_df.groupby("State").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        if not state_summary_insights.empty:
            highest_sales_state = state_summary_insights["Sales"].idxmax()
            highest_profit_state = state_summary_insights["Profit"].idxmax()
            lowest_profit_state = state_summary_insights["Profit"].idxmin()
            st.write(f"🔹 **{highest_profit_state} is the most profitable state.**")
            st.write(f"🔹 **{lowest_profit_state} has the lowest state profit.**")
            if highest_sales_state != highest_profit_state:
                st.write(
                    f"🔹 **{highest_sales_state} generates the most sales, but {highest_profit_state} generates the most profit.**"
                )

    if "City" in filtered_df.columns:
        city_profit = filtered_df.groupby("City")["Profit"].sum()
        if not city_profit.empty:
            st.write(f"🔹 **{city_profit.idxmax()} is the most profitable city.**")

    st.markdown("---")
    st.subheader("🧠 Business Recommendations")
    recommendations = []

    if "Category" in filtered_df.columns:
        category_profit = filtered_df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
        if not category_profit.empty:
            recommendations.append(
                f"Focus on **{category_profit.index[0]}** because it currently generates the highest profit."
            )

    if "Region" in filtered_df.columns:
        region_profit = filtered_df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
        if not region_profit.empty:
            recommendations.append(
                f"Prioritize high-performing regions such as **{region_profit.index[0]}**."
            )

    if "Sub-Category" in filtered_df.columns:
        subcategory_profit = filtered_df.groupby("Sub-Category")["Profit"].sum().sort_values()
        if not subcategory_profit.empty:
            recommendations.append(
                f"Review **{subcategory_profit.index[0]}** because it has the lowest profit."
            )

    if "Discount" in filtered_df.columns and "Profit" in filtered_df.columns:
        discount_insight_data = filtered_df.copy()
        discount_insight_data["Discount Range"] = pd.cut(
            discount_insight_data["Discount"],
            bins=[-0.01, 0, 0.10, 0.20, 0.30, 0.40, 1.00],
            labels=["0%", "1-10%", "11-20%", "21-30%", "31-40%", "40%+"],
        )
        discount_profit_means = discount_insight_data.groupby(
            "Discount Range", observed=False
        )["Profit"].mean().dropna()
        if len(discount_profit_means) >= 2:
            low_discount_profit = discount_profit_means.iloc[0]
            high_discount_profit = discount_profit_means.iloc[-1]
            if high_discount_profit < low_discount_profit:
                recommendations.append(
                    "High discount levels are associated with weaker average profitability in the selected data."
                )
            else:
                recommendations.append(
                    "Higher discount ranges currently maintain or exceed the average profit of the lowest discount range."
                )

    if "State" in filtered_df.columns:
        state_profit = filtered_df.groupby("State")["Profit"].sum().sort_values(ascending=False)
        if not state_profit.empty:
            recommendations.append(
                f"Use successful states such as **{state_profit.index[0]}** as benchmarks for improving lower-performing markets."
            )

    for number, recommendation in enumerate(recommendations[:5], start=1):
        st.markdown(f"**{number}.** {recommendation}")


# ============================================================
# 14. FILTERED DATASET + DOWNLOAD
# ============================================================

st.markdown("---")
with st.expander("📄 View Filtered Dataset"):
    st.dataframe(filtered_df, width="stretch", height=400)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_retail_business_data.csv",
    mime="text/csv",
)

st.download_button(
    label="⬇️ Download Business Summary CSV",
    data=summary_csv_data,
    file_name="business_summary.csv",
    mime="text/csv",
)


# ============================================================
# 15. FOOTER
# ============================================================

st.markdown("---")
st.caption("Retail Business Analytics Dashboard")
st.caption("Built with Python • Pandas • Plotly • Streamlit")
