# plots.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
import wallet  

sns.set_theme(style="whitegrid")

def _prepare_data_copy():
    df = wallet.get_all_transactions().copy()
    df['date'] = pd.to_datetime(df['date'])
    return df

def plot_expenses_by_category_fig():
    """
    Retourne une matplotlib.figure.Figure pour les dépenses par catégorie.
    """
    df = _prepare_data_copy()
    expenses = df[df["type"] == "expense"].groupby("category")["amount"].sum().reset_index()
    fig = Figure(figsize=(8,5), dpi=100)
    ax = fig.add_subplot(111)
    sns.barplot(x="category", y="amount", data=expenses, palette="Reds_d", ax=ax)
    ax.set_title("Expenses by Category", fontsize=14, fontweight="bold")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")
    ax.tick_params(axis='x', rotation=30)
    # annotations
    for i, row in expenses.iterrows():
        ax.text(i, row.amount + 0.01 * expenses["amount"].max(), f"{row.amount:.2f}", ha='center', va='bottom', fontsize=9)
    fig.tight_layout()
    return fig

def plot_income_by_category_fig():
    """
    Retourne une Figure pour les revenus par catégorie.
    """
    df = _prepare_data_copy()
    income = df[df["type"] == "income"].groupby("category")["amount"].sum().reset_index()
    fig = Figure(figsize=(8,5), dpi=100)
    ax = fig.add_subplot(111)
    sns.barplot(x="category", y="amount", data=income, palette="Greens_d", ax=ax)
    ax.set_title("Income by Category", fontsize=14, fontweight="bold")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")
    ax.tick_params(axis='x', rotation=30)
    for i, row in income.iterrows():
        ax.text(i, row.amount + 0.01 * income["amount"].max(), f"{row.amount:.2f}", ha='center', va='bottom', fontsize=9)
    fig.tight_layout()
    return fig

def plot_monthly_balance_fig():
    """
    Retourne une Figure montrant la balance mensuelle (income - expense).
    """
    df = _prepare_data_copy()
    df['month'] = df['date'].dt.to_period('M').dt.to_timestamp()
    monthly = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
    monthly['balance'] = monthly.get('income', 0) - monthly.get('expense', 0)
    monthly = monthly.reset_index()

    fig = Figure(figsize=(10,5), dpi=100)
    ax = fig.add_subplot(111)
    sns.lineplot(x="month", y="balance", data=monthly, marker="o", ax=ax)
    ax.set_title("Monthly Balance", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Balance")
    ax.tick_params(axis='x', rotation=35)
    fig.tight_layout()
    return fig

def plot_income_vs_expenses_monthly_fig():
    """
    Retourne une Figure comparant revenus vs dépenses mensuels.
    """
    df = _prepare_data_copy()
    df['month'] = df['date'].dt.to_period('M').dt.to_timestamp()
    monthly = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0).reset_index()

    # S'assurer que les colonnes existent
    if 'income' not in monthly.columns:
        monthly['income'] = 0
    if 'expense' not in monthly.columns:
        monthly['expense'] = 0

    melted = monthly.melt(id_vars="month", value_vars=["income", "expense"], var_name="Type", value_name="Amount")

    fig = Figure(figsize=(10,5), dpi=100)
    ax = fig.add_subplot(111)
    sns.barplot(x="month", y="Amount", hue="Type", data=melted, palette={"income":"#2ca02c","expense":"#d62728"}, ax=ax)
    ax.set_title("Monthly Income vs Expenses", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.tick_params(axis='x', rotation=35)
    ax.legend(title="Type")
    fig.tight_layout()
    return fig
