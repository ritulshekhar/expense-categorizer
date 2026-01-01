import streamlit as st
import pandas as pd
import re
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Smart Expense Categorizer",
    page_icon="💸",
    layout="wide"
)

# ------------------ THEME TOGGLE ------------------
theme = st.sidebar.radio(
    "🎨 Theme",
    ["Light Pastel", "Dark Pastel"],
    horizontal=True
)

# ------------------ THEME CSS ------------------
if theme == "Light Pastel":
    bg = "#F6F7FB"
    card = "#FFFFFF"
    text = "#1F2937"
    muted = "#6B7280"
    primary = "#A5B4FC"
else:
    bg = "#0F172A"
    card = "#1E293B"
    text = "#E5E7EB"
    muted = "#9CA3AF"
    primary = "#818CF8"

st.markdown(f"""
<style>
.stApp {{
    background-color: {bg};
}}

h1, h2, h3, h4 {{
    color: {text};
}}

p {{
    color: {muted};
}}

div[data-testid="stMetric"],
div[data-testid="stPlotlyChart"],
div[data-testid="stDataFrame"],
div[data-testid="stFileUploader"] {{
    background-color: {card};
    border-radius: 16px;
    padding: 1.2rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}}

button[kind="primary"] {{
    background-color: {primary};
    color: white;
    border-radius: 10px;
    border: none;
}}

thead tr th {{
    background-color: rgba(165,180,252,0.15);
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
<h1>💸 Smart Expense Categorizer</h1>
<p>Upload your bank statement and instantly understand your spending.</p>
""", unsafe_allow_html=True)

# ------------------ HELPERS ------------------
def clean_description(text):
    text = str(text).lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    return text.strip()

RULES = {
    "Food": ["zomato", "swiggy", "restaurant", "cafe"],
    "Shopping": ["amazon", "flipkart", "myntra"],
    "Transport": ["uber", "ola", "metro", "fuel"],
    "Bills": ["electricity", "recharge", "bill", "internet"],
    "Subscriptions": ["netflix", "spotify", "prime"]
}

def categorize(text):
    for cat, kws in RULES.items():
        for kw in kws:
            if kw in text:
                return cat
    return "Others"

# ------------------ FILE UPLOAD ------------------
uploaded = st.file_uploader("📄 Upload Bank Statement CSV", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    df.columns = df.columns.str.lower()

    df['date'] = pd.to_datetime(df['date'])
    df = df[df['amount'] < 0]
    df['amount'] = df['amount'].abs()

    df['clean_desc'] = df['description'].apply(clean_description)
    df['category'] = df['clean_desc'].apply(categorize)

    # ------------------ MONTH FILTER ------------------
    df['month'] = df['date'].dt.to_period('M').astype(str)
    months = ["All"] + sorted(df['month'].unique().tolist())

    selected_month = st.selectbox("📅 Filter by Month", months)

    if selected_month != "All":
        df = df[df['month'] == selected_month]

    # ------------------ METRICS ------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Spend", f"₹ {df['amount'].sum():,.0f}")
    col2.metric("📊 Categories", df['category'].nunique())
    col3.metric("🧾 Transactions", len(df))

    # ------------------ CHARTS ------------------
    col1, col2 = st.columns(2)

    with col1:
        pie = px.pie(
            df,
            names="category",
            values="amount",
            hole=0.45,
            color_discrete_sequence=[
                "#A5B4FC", "#FBCFE8", "#BBF7D0", "#FDE68A", "#BFDBFE"
            ]
        )
        pie.update_layout(
            title="Spending by Category",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=text)
        )
        st.plotly_chart(pie, use_container_width=True)

    with col2:
        bar = px.bar(
            df.groupby('category')['amount'].sum().reset_index(),
            x="category",
            y="amount",
            color="category",
            color_discrete_sequence=[
                "#A5B4FC", "#FBCFE8", "#BBF7D0", "#FDE68A", "#BFDBFE"
            ]
        )
        bar.update_layout(
            title="Total Spend per Category",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=text),
            showlegend=False
        )
        st.plotly_chart(bar, use_container_width=True)

    # ------------------ TABLE ------------------
    st.subheader("📄 Categorized Transactions")
    st.dataframe(
        df[['date', 'description', 'category', 'amount']],
        use_container_width=True,
        height=420
    )

    # ------------------ DOWNLOAD ------------------
    st.download_button(
        "⬇️ Download Categorized CSV",
        df.to_csv(index=False),
        "categorized_expenses.csv",
        type="primary"
    )

else:
    st.info("Upload a CSV to get started.")
