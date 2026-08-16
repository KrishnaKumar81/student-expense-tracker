import streamlit as st
import requests
import pandas as pd
import plotly.express as px


# FastAPI backend address
API_URL = "http://127.0.0.1:8000"


# Page configuration
st.set_page_config(
    page_title="Student Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# Title
st.title("💰 Student Expense Tracker")

st.write("Track and analyze your daily expenses.")


# -----------------------------------
# Add Expense
# -----------------------------------

st.header("Add Expense")

category = st.selectbox(
    "Category",
    [
        "Food",
        "Transport",
        "Education",
        "Shopping",
        "Entertainment",
        "Other"
    ]
)

amount = st.number_input(
    "Amount",
    min_value=0.0,
    step=10.0
)

date = st.date_input("Date")

description = st.text_input("Description")


if st.button("Add Expense"):

    response = requests.post(
        f"{API_URL}/expenses",
        params={
            "category": category,
            "amount": amount,
            "date": str(date),
            "description": description
        }
    )

    if response.status_code == 200:
        st.success("Expense added successfully!")

    else:
        st.error("Something went wrong.")


# -----------------------------------
# Get Expenses
# -----------------------------------

response = requests.get(
    f"{API_URL}/expenses"
)


if response.status_code == 200:

    expenses = response.json()

else:

    expenses = []


# -----------------------------------
# Display Expenses
# -----------------------------------

if expenses:

    df = pd.DataFrame(expenses)


    # Total expense
    total_expense = df["amount"].sum()

    st.header("Expense Summary")

    st.metric(
        "Total Expenses",
        f"₹{total_expense:,.2f}"
    )


    # -----------------------------------
    # Category Summary
    # -----------------------------------

    category_summary = (
        df.groupby("category")["amount"]
        .sum()
        .reset_index()
    )


    # -----------------------------------
    # Pie Chart
    # -----------------------------------

    fig = px.pie(
        category_summary,
        names="category",
        values="amount",
        title="Expenses by Category"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -----------------------------------
    # Expense Table
    # -----------------------------------

    st.header("All Expenses")

st.dataframe(
    df,
    use_container_width=True
)


# -----------------------------------
# Delete Expense
# -----------------------------------

st.subheader("Delete Expense")

expense_id = st.number_input(
    "Enter Expense ID",
    min_value=1,
    step=1
)


if st.button("Delete Expense"):

    response = requests.delete(
        f"{API_URL}/expenses/{int(expense_id)}"
    )

    if response.status_code == 200:

        st.success("Expense deleted successfully!")

        st.rerun()

    else:

        st.error("Could not delete expense.")

else:

    st.info("No expenses added yet.")