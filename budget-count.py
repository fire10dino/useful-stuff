import streamlit as st
import pandas as pd

st.title("💰 Weekly Budget Tracker")

# Initialize session state
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Category", "Amount"])
if "last_category" not in st.session_state:
    st.session_state.last_category = "Food"
if "last_amount" not in st.session_state:
    st.session_state.last_amount = 0.0
if "custom_category" not in st.session_state:
    st.session_state.custom_category = ""
if "start_budget" not in st.session_state:
    st.session_state.start_budget = 0.0

categories = ["Food", "Transportation", "Games", "Other"]

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Controls")

    # Starting budget
    st.session_state.start_budget = st.number_input(
        "Starting Budget",
        min_value=0.0,
        step=10.0,
        value=st.session_state.start_budget,
    )

    # Add expense form
    with st.form("add_expense_form"):
        selected_category = st.selectbox(
            "Category",
            categories,
            index=categories.index(st.session_state.last_category),
        )

        custom_name = st.text_input(
            "Custom category (used only if 'Other' selected)",
            value=st.session_state.custom_category,
        )

        exp_amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=1.0,
            value=st.session_state.last_amount,
        )

        add_expense = st.form_submit_button("➕ Add Expense")

        if add_expense and exp_amount > 0:
            # Final category
            if selected_category == "Other":
                category = custom_name.strip() or "Other"
            else:
                category = selected_category

            # Save the expense
            new_expense = pd.DataFrame({"Category": [category], "Amount": [exp_amount]})
            st.session_state.expenses = pd.concat(
                [st.session_state.expenses, new_expense], ignore_index=True
            )

            # Reset inputs for next run
            st.session_state.last_category = "Food"
            st.session_state.last_amount = 0.0
            st.session_state.custom_category = ""

    # Reset button
    if st.button("♻️ Reset All"):
        st.session_state.expenses = pd.DataFrame(columns=["Category", "Amount"])
        st.session_state.last_category = "Food"
        st.session_state.last_amount = 0.0
        st.session_state.custom_category = ""
        st.session_state.start_budget = 0.0

# Display expenses
if not st.session_state.expenses.empty:
    st.subheader("📊 Expenses Table")
    st.dataframe(st.session_state.expenses, use_container_width=True)

    total_spent = st.session_state.expenses["Amount"].sum()
    remaining = st.session_state.start_budget - total_spent

    st.write(f"**Total Spent:** {total_spent}")
    if remaining < 0:
        st.error(f"**Remaining Budget:** {remaining} (⚠️ Overspent!)")
    else:
        st.success(f"**Remaining Budget:** {remaining}")

    # Bar chart
    st.subheader("📈 Expenses by Category")
    category_summary = st.session_state.expenses.groupby("Category")["Amount"].sum()
    st.bar_chart(category_summary)
else:
    st.info("No expenses yet. Use the sidebar to add some.")
