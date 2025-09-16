import streamlit as st
import pandas as pd
import altair as alt

st.title("💰 Weekly Budget Tracker")

# Initialize session state
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Category", "Amount"])
if "starting_budget" not in st.session_state:
    st.session_state.starting_budget = 0.0
if "custom_category" not in st.session_state:
    st.session_state.custom_category = ""

# -------- Sidebar Controls --------
st.sidebar.header("⚙️ Controls")

# Starting budget
st.session_state.starting_budget = st.sidebar.number_input(
    "💵 Starting Budget",
    min_value=0.0,
    step=10.0,
    value=st.session_state.starting_budget,
)

# Expense input
st.sidebar.subheader("➖ Add Expense")
categories = ["Food", "Transportation", "Games", "Other"]

with st.sidebar.form("add_expense_form", clear_on_submit=True):
    selected_category = st.selectbox("Category", categories)
    
    # Custom category input (always editable)
    custom_category = st.text_input(
        "Custom category (used only if 'Other' selected)",
        value=st.session_state.custom_category
    )
    st.session_state.custom_category = custom_category
    
    # Determine final category
    if selected_category == "Other":
        category = custom_category.strip() or "Other"
    else:
        category = selected_category
    
    exp_amount = st.number_input("Amount", min_value=0.0, step=1.0)
    
    add_expense = st.form_submit_button("➕ Add Expense")
    
    if add_expense and category and exp_amount > 0:
        new_expense = pd.DataFrame({"Category": [category], "Amount": [exp_amount]})
        st.session_state.expenses = pd.concat(
            [st.session_state.expenses, new_expense], ignore_index=True
        )

# -------- Expense Table --------
if not st.session_state.expenses.empty:
    st.subheader("📊 Expense Table (Editable)")
    expenses_edited = st.data_editor(
        st.session_state.expenses,
        num_rows="dynamic",
        use_container_width=True
    )
    st.session_state.expenses = expenses_edited
    total_expenses = st.session_state.expenses["Amount"].sum()
else:
    total_expenses = 0
    st.info("No expenses added yet.")

# -------- Summary --------
st.header("📌 Summary")
remaining_budget = st.session_state.starting_budget - total_expenses
st.write(f"**Starting Budget:** {st.session_state.starting_budget}")
st.write(f"**Total Expenses:** {total_expenses}")
st.write(f"### ✅ Remaining Budget: {remaining_budget}")

# -------- Graph --------
if not st.session_state.expenses.empty:
    st.subheader("📈 Expenses by Category")
    exp_chart = (
        alt.Chart(st.session_state.expenses)
        .mark_bar()
        .encode(x="Category", y="Amount", tooltip=["Category", "Amount"])
    )
    st.altair_chart(exp_chart, use_container_width=True)
