import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import calendar
from utils import load_data, save_expense, save_budget, initialize_data

# Page configuration
st.set_page_config(page_title="Personal Budget Planner", layout="wide")

# Initialize session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = load_data('expenses')
if 'budgets' not in st.session_state:
    st.session_state.budgets = load_data('budgets')

# Initialize data files if they don't exist
initialize_data()

# Main title
st.title("💰 Personal Budget Planner")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Add Expense", "Budget Planning"])

if page == "Dashboard":
    # Dashboard layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monthly Overview")
        current_month = datetime.now().strftime('%Y-%m')
        
        # Filter current month's expenses
        monthly_expenses = st.session_state.expenses[
            st.session_state.expenses['date'].str.startswith(current_month)
        ]
        
        # Calculate total expenses
        total_expenses = monthly_expenses['amount'].sum()
        st.metric("Total Expenses", f"${total_expenses:,.2f}")
        
        # Expenses by category
        category_expenses = monthly_expenses.groupby('category')['amount'].sum()
        
        # Pie chart
        fig = px.pie(
            values=category_expenses.values,
            names=category_expenses.index,
            title="Expenses by Category"
        )
        st.plotly_chart(fig)
    
    with col2:
        st.subheader("Budget vs Actual")
        current_budget = st.session_state.budgets.iloc[-1] if not st.session_state.budgets.empty else pd.Series()
        
        # Create comparison chart
        categories = monthly_expenses['category'].unique()
        budget_values = []
        actual_values = []
        
        for cat in categories:
            budget_values.append(float(current_budget.get(cat, 0)))
            actual_values.append(float(monthly_expenses[monthly_expenses['category'] == cat]['amount'].sum()))
        
        fig = go.Figure(data=[
            go.Bar(name='Budget', x=categories, y=budget_values),
            go.Bar(name='Actual', x=categories, y=actual_values)
        ])
        fig.update_layout(barmode='group', title="Budget vs Actual Spending")
        st.plotly_chart(fig)

elif page == "Add Expense":
    st.subheader("Add New Expense")
    
    with st.form("expense_form"):
        date = st.date_input("Date", datetime.now())
        category = st.selectbox(
            "Category",
            ["Housing", "Transportation", "Food", "Utilities", "Entertainment", "Healthcare", "Shopping", "Other"]
        )
        description = st.text_input("Description")
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
        
        if st.form_submit_button("Add Expense"):
            save_expense(date.strftime('%Y-%m-%d'), category, description, amount)
            st.success("Expense added successfully!")
            st.session_state.expenses = load_data('expenses')

elif page == "Budget Planning":
    st.subheader("Monthly Budget Planning")
    
    with st.form("budget_form"):
        st.write("Set budget limits for each category")
        housing = st.number_input("Housing ($)", min_value=0.0, step=50.0)
        transportation = st.number_input("Transportation ($)", min_value=0.0, step=50.0)
        food = st.number_input("Food ($)", min_value=0.0, step=50.0)
        utilities = st.number_input("Utilities ($)", min_value=0.0, step=50.0)
        entertainment = st.number_input("Entertainment ($)", min_value=0.0, step=50.0)
        healthcare = st.number_input("Healthcare ($)", min_value=0.0, step=50.0)
        shopping = st.number_input("Shopping ($)", min_value=0.0, step=50.0)
        other = st.number_input("Other ($)", min_value=0.0, step=50.0)
        
        if st.form_submit_button("Save Budget"):
            budget_data = {
                'Housing': housing,
                'Transportation': transportation,
                'Food': food,
                'Utilities': utilities,
                'Entertainment': entertainment,
                'Healthcare': healthcare,
                'Shopping': shopping,
                'Other': other
            }
            save_budget(budget_data)
            st.success("Budget updated successfully!")
            st.session_state.budgets = load_data('budgets')

# Download data section
st.sidebar.subheader("Export Data")
if st.sidebar.button("Download Expenses CSV"):
    csv = st.session_state.expenses.to_csv(index=False)
    st.sidebar.download_button(
        label="Click to Download",
        data=csv,
        file_name="expenses.csv",
        mime="text/csv"
    )
