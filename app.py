import streamlit as st
import pandas as pd
# NEW: Import fpgrowth, which is more memory-efficient than apriori
from mlxtend.frequent_patterns import fpgrowth, association_rules
import openpyxl

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Market Basket Analysis",
    page_icon="🛒",
    layout="wide",
)

# --- APP TITLE AND DESCRIPTION ---
st.title("🛒 Market Basket Analysis Application")
st.markdown("""
This application performs Market Basket Analysis to discover which products are frequently bought together. It uses the **FP-Growth** algorithm, which is optimized for large datasets.

**Instructions:**
1.  **Upload your data** in Excel (`.xlsx`) or CSV (`.csv`) format using the sidebar.
2.  Adjust the analysis parameters in the sidebar to control the results.
3.  Click the **Analyze Data** button to generate and view the frequent itemsets and association rules.
""")


# --- DATA LOADING AND CACHING ---
@st.cache_data
def load_data(file):
    """
    Loads and preprocesses transactional data from an uploaded file.
    """
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, encoding='latin1')
        else:
            df = pd.read_excel(file, engine='openpyxl')
    except Exception as e:
        st.error(f"Error loading the data file: {e}")
        return None

    required_cols = ['InvoiceNo', 'Description', 'Quantity']
    if not all(col in df.columns for col in required_cols):
        st.error(f"The uploaded file must contain the following columns: {', '.join(required_cols)}")
        return None

    df['Description'] = df['Description'].str.strip()
    df.dropna(axis=0, subset=['InvoiceNo'], inplace=True)
    df['InvoiceNo'] = df['InvoiceNo'].astype('str')
    df = df[~df['InvoiceNo'].str.contains('C')]
    df = df[df['Quantity'] > 0]

    return df


# --- ANALYSIS FUNCTION ---
def perform_market_basket_analysis(df, min_support, min_threshold):
    """
    Performs market basket analysis using the FP-Growth algorithm.
    """
    # --- ONE-HOT ENCODING THE DATA ---
    basket = (df
              .groupby(['InvoiceNo', 'Description'])['Quantity']
              .sum().unstack().reset_index().fillna(0)
              .set_index('InvoiceNo'))

    def encode_units(x):
        return 1 if x >= 1 else 0

    basket_sets = basket.applymap(encode_units)

    # NEW: Remove items that have a low frequency to reduce memory usage
    # This is a critical step for large datasets
    min_item_frequency = 5  # You can make this a parameter if you want
    sparse_items = [col for col, val in basket_sets.sum().items() if val < min_item_frequency]
    basket_sets.drop(sparse_items, axis=1, inplace=True)
    st.write(f"Removed {len(sparse_items)} infrequent items. Analyzing the remaining {basket_sets.shape[1]} items.")

    # --- FP-GROWTH ALGORITHM ---
    # NEW: Using fpgrowth instead of apriori
    frequent_itemsets = fpgrowth(basket_sets, min_support=min_support, use_colnames=True)

    # --- GENERATE ASSOCIATION RULES ---
    # Using "lift" as the metric to find interesting rules
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_threshold)

    return frequent_itemsets, rules


# --- SIDEBAR FOR USER INPUTS ---
with st.sidebar:
    st.header("⚙️ Settings")

    uploaded_file = st.file_uploader("Upload your transaction data", type=["xlsx", "csv"])

    if uploaded_file:
        st.subheader("Analysis Parameters")

        # NOTE: With large datasets, you need a much smaller min_support
        min_support = st.slider(
            "Minimum Support", 0.001, 0.1, 0.01, 0.001, format="%.3f",
            help="The minimum support for an itemset to be considered frequent. For large datasets, this value should be low."
        )
        min_lift = st.slider(
            "Minimum Lift", 0.5, 3.0, 1.0, 0.1,
            help="The minimum lift for an association rule. Lift > 1 suggests a positive correlation."
        )

        analyze_button = st.button("Analyze Data", type="primary")

# --- MAIN APPLICATION LOGIC ---
if 'uploaded_file' in locals() and uploaded_file:
    st.header("Data Preview")
    df = load_data(uploaded_file)

    if df is not None:
        st.dataframe(df.head(10))

        if 'analyze_button' in locals() and analyze_button:
            with st.spinner('Performing analysis... This may take a moment on large datasets.'):
                frequent_itemsets, rules = perform_market_basket_analysis(df, min_support, min_lift)

            st.success("Analysis complete!")

            st.header("📊 Frequent Itemsets")
            st.write(
                "These are the sets of items that are frequently purchased together, sorted by their support value.")
            st.dataframe(frequent_itemsets.sort_values(by="support", ascending=False))

            st.header("🔗 Generated Association Rules")
            st.write(
                "'Antecedents' -> 'Consequents' means that customers who bought the antecedent item(s) also tend to buy the consequent item(s).")
            st.dataframe(rules.sort_values(by="lift", ascending=False))
else:
    st.info("Upload a data file using the sidebar to begin the analysis.")