import streamlit as st
import pandas as pd
import re
import json
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Expense Categorizer",
    layout="wide"
)

# ------------------ LOAD CATEGORY RULES ------------------
with open("assets/categories.json", "r") as f:
    CATEGORY_RULES = json.load(f)

# ------------------ THEME TOGGLE ------------------
theme = st.sidebar.radio(
    "Theme",
    ["Light Mode", "Dark Mode"],
    horizontal=True
)

# ------------------ COLOR PALETTE (CUSTOM) ------------------
if theme == "Light Mode":
    bg = "#E8D8C4"        # Light beige
    card = "#F3EBDD"
    text = "#561C24"      # Wine
    muted = "#6D2932"
    primary = "#6D2932"
    accent = "#C7B7A3"
else:
    bg = "#561C24"        # Wine background
    card = "#6D2932"
    text = "#E8D8C4"
    muted = "#C7B7A3"
    primary = "#C7B7A3"
    accent = "#E8D8C4"

# ------------------ GLOBAL CSS ------------------
st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(180deg, {bg} 0%, #C7B7A3 100%);
}}

h1, h2, h3, h4 {{
    color: {text};
    font-weight: 700;
}}

p, span, label {{
    color: {muted};
}}

div[data-testid="stMetric"],
div[data-testid="stPlotlyChart"],
div[data-testid="stDataFrame"],
div[data-testid="stFileUploader"] {{
    background-color: {card};
    border-radius: 18px;
    padding: 1.3rem;
    box-shadow: 0 12px 30px rgba(0,0,0,0.18);
}}

button[kind="primary"] {{
    background-color: {primary};
    color: {"#E8D8C4" if theme == "Dark Mode" else "#FFFFFF"};
    border-radius: 12px;
    border: none;
    font-weight: 600;
}}

button[kind="primary"]:hover {{
    opacity: 0.9;
}}

thead tr th {{
    background-color: {accent};
    color: {text};
}}

@media (max-width: 768px) {{
    h1 {{
        font-size: 1.6rem;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("""
<h1>Expense Categorizer</h1>
<p>Upload your bank statement and instantly understand your spending patterns.</p>
""", unsafe_allow_html=True)

# ------------------ HELPERS ------------------
def clean_description(text):
    text = str(text).lower()
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    return text.strip()

def categorize(text):
    for category, data in CATEGORY_RULES.items():
        for kw in data["keywords"]:
            if kw in text:
                return category
    return "Others"

# ------------------ FILE UPLOAD ------------------
uploaded = st.file_uploader("Upload Bank Statement CSV", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    df.columns = df.columns.str.lower()

    df["date"] = pd.to_datetime(df["date"])
    df = df[df["amount"] < 0]
    df["amount"] = df["amount"].abs()

    df["clean_desc"] = df["description"].apply(clean_description)
    df["category"] = df["clean_desc"].apply(categorize)

    # ------------------ MONTH FILTER ------------------
    df["month"] = df["date"].dt.to_period("M").astype(str)
    months = ["All"] + sorted(df["month"].unique().tolist())
    selected_month = st.selectbox("Filter by Month", months)

    if selected_month != "All":
        df = df[df["month"] == selected_month]

    # ------------------ METRICS ------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spend", f"₹ {df['amount'].sum():,.0f}")
    col2.metric("Categories", df["category"].nunique())
    col3.metric("Transactions", len(df))

    # ------------------ CHARTS ------------------
    palette = ["#561C24", "#6D2932", "#C7B7A3", "#E8D8C4"]

    col1, col2 = st.columns(2)

    with col1:
        pie = px.pie(
            df,
            names="category",
            values="amount",
            hole=0.45,
            color_discrete_sequence=palette
        )
        pie.update_layout(
            title="Spending by Category",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=text)
        )
        st.plotly_chart(pie, use_container_width=True)

    with col2:
        bar = px.bar(
            df.groupby("category")["amount"].sum().reset_index(),
            x="category",
            y="amount",
            color="category",
            color_discrete_sequence=palette
        )
        bar.update_layout(
            title="Total Spend per Category",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=text),
            showlegend=False
        )
        st.plotly_chart(bar, use_container_width=True)

    # ------------------ TABLE ------------------
    st.subheader("Categorized Transactions")
    st.dataframe(
        df[["date", "description", "category", "amount"]],
        use_container_width=True,
        height=420
    )

    # ------------------ SUGGEST CATEGORY (FEEDBACK LOOP) ------------------
    st.subheader("Suggest Category for Unmatched Transactions")

    unmatched = df[df["category"] == "Others"]

    if not unmatched.empty:
        for idx, row in unmatched.iterrows():
            with st.expander(row["description"]):
                suggestion = st.selectbox(
                    "Select correct category",
                    options=list(CATEGORY_RULES.keys()),
                    key=f"suggest_{idx}"
                )
                if st.button("Submit", key=f"submit_{idx}"):
                    st.success(
                        f"Suggestion saved: '{suggestion}' for '{row['description']}'"
                    )
    else:
        st.info("All transactions were categorized successfully.")

    # ------------------ DOWNLOAD ------------------
    st.download_button(
        "Download Categorized CSV",
        df.to_csv(index=False),
        "categorized_expenses.csv",
        type="primary"
    )

else:
    st.info("Upload a CSV to get started.")
