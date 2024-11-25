import pandas as pd
import os

def initialize_data():
    """Initialize data files if they don't exist"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Initialize expenses.csv
    if not os.path.exists('data/expenses.csv'):
        df = pd.DataFrame(columns=['date', 'category', 'description', 'amount'])
        df.to_csv('data/expenses.csv', index=False)
    
    # Initialize budgets.csv
    if not os.path.exists('data/budgets.csv'):
        categories = ['Housing', 'Transportation', 'Food', 'Utilities', 
                     'Entertainment', 'Healthcare', 'Shopping', 'Other']
        df = pd.DataFrame(columns=categories)
        df.to_csv('data/budgets.csv', index=False)

def load_data(data_type):
    """Load data from CSV files"""
    if data_type == 'expenses':
        return pd.read_csv('data/expenses.csv')
    elif data_type == 'budgets':
        return pd.read_csv('data/budgets.csv')

def save_expense(date, category, description, amount):
    """Save new expense to CSV"""
    df = load_data('expenses')
    new_expense = pd.DataFrame({
        'date': [date],
        'category': [category],
        'description': [description],
        'amount': [amount]
    })
    df = pd.concat([df, new_expense], ignore_index=True)
    df.to_csv('data/expenses.csv', index=False)

def save_budget(budget_data):
    """Save new budget to CSV"""
    df = load_data('budgets')
    new_budget = pd.DataFrame([budget_data])
    df = pd.concat([df, new_budget], ignore_index=True)
    df.to_csv('data/budgets.csv', index=False)
