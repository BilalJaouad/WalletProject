"""
Module de prédiction financière
Prédit les revenus ou dépenses futurs à partir de l'historique.
Utilise sklearn pour la régression linéaire ou d'autres modèles.
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np
import wallet  

def prepare_monthly_data():
    """
    Retourne un DataFrame avec les totaux mensuels pour income et expense.
    Colonnes : month (datetime), income, expense
    """
    df = wallet.get_all_transactions().copy()
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').dt.to_timestamp()
    monthly = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0).reset_index()
    if 'income' not in monthly.columns:
        monthly['income'] = 0
    if 'expense' not in monthly.columns:
        monthly['expense'] = 0
    monthly['balance'] = monthly['income'] - monthly['expense']
    return monthly

def predict_next_month_income(model_type="linear"):
    """
    Prédit le revenu du prochain mois.
    model_type: 'linear' (actuellement)
    """
    df = prepare_monthly_data()
    if len(df) < 2:
        return None  # pas assez de données

    # Feature: mois indexé
    df['month_idx'] = np.arange(len(df))
    X = df[['month_idx']]
    y = df['income']

    model = LinearRegression()
    model.fit(X, y)

    next_month_idx = np.array([[len(df)]])
    prediction = model.predict(next_month_idx)
    return max(prediction[0], 0)

def predict_next_month_expense():
    """
    Prédit les dépenses du mois prochain via régression linéaire.
    """
    df = prepare_monthly_data()
    if len(df) < 2:
        return None

    df['month_idx'] = np.arange(len(df))
    X = df[['month_idx']]
    y = df['expense']

    model = LinearRegression()
    model.fit(X, y)

    next_month_idx = np.array([[len(df)]])
    prediction = model.predict(next_month_idx)
    return max(prediction[0], 0)

def predict_next_month_balance():
    """
    Prédit la balance du mois prochain.
    """
    income_pred = predict_next_month_income()
    expense_pred = predict_next_month_expense()
    if income_pred is None or expense_pred is None:
        return None
    return income_pred - expense_pred

def predict_income_trend(months_ahead=6):
    """
    Prédit le revenu pour les `months_ahead` prochains mois et retourne une liste.
    """
    df = prepare_monthly_data()
    if len(df) < 2:
        return []

    df['month_idx'] = np.arange(len(df))
    X = df[['month_idx']]
    y = df['income']
    model = LinearRegression()
    model.fit(X, y)

    future_idx = np.arange(len(df), len(df)+months_ahead).reshape(-1,1)
    pred = model.predict(future_idx)
    pred = [max(p,0) for p in pred]
    return pred

def predict_expense_trend(months_ahead=6):
    """
    Prédit les dépenses pour les `months_ahead` prochains mois.
    """
    df = prepare_monthly_data()
    if len(df) < 2:
        return []

    df['month_idx'] = np.arange(len(df))
    X = df[['month_idx']]
    y = df['expense']
    model = LinearRegression()
    model.fit(X, y)

    future_idx = np.arange(len(df), len(df)+months_ahead).reshape(-1,1)
    pred = model.predict(future_idx)
    pred = [max(p,0) for p in pred]
    return pred

def predict_balance_trend(months_ahead=6):
    """
    Prédit la balance pour les `months_ahead` prochains mois.
    """
    income_pred = predict_income_trend(months_ahead)
    expense_pred = predict_expense_trend(months_ahead)
    return [i - e for i, e in zip(income_pred, expense_pred)]
