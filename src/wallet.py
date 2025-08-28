import pandas as pd
from fpdf import FPDF


PATH = r"WalletProject\data\transactions.csv"
data = pd.read_csv(PATH)



#print(data.head())
#print(data.describe())
#print(data.info())   
#expenses = data[data["type"] == "expense"]
#print(expenses.head())
#big_income = data[(data["type"] == "income") & (data["amount"] > 300)]
#print(big_income)

#total_expenses = expenses["amount"]
#print(total_expenses.sum())
#icome = data[data["type"] == "income"]
#icome = icome["amount"].sum()
#print(icome)


#print(data[data["type"]=="expense"].groupby("category")["amount"].sum())    
#print(data.groupby("date")["amount"].mean())

def get_expenses_by_category(category):
    expenses = data[(data["type"] == "expense") & (data["category"] == category)]
    return expenses["amount"].sum()

def get_income_by_category(category):
    income = data[(data["type"] == "income") & (data["category"] == category)]
    return income["amount"].sum()

def get_total_expenses():
    expenses = data[data["type"] == "expense"]
    return expenses["amount"].sum()

def get_total_income():
    income = data[data["type"] == "income"]
    return income["amount"].sum()

def get_balance():
    return get_total_income() - get_total_expenses()

def add_transaction(date, amount, type, category, description, Currency="MAD"):
    global data
    new_transaction = pd.DataFrame({
        "date": [date],
        "amount": [amount],
        "type": [type],
        "category": [category],
        "description": [description] ,
        "Currency": [Currency]
    })
    data = pd.concat([data, new_transaction], ignore_index=True)
    data.to_csv(PATH, index=False)

def delete_transaction(index):
    global data
    if 0 <= index < len(data):
        data = data.drop(index).reset_index(drop=True)
        data.to_csv(PATH, index=False)
    else:
        print("Invalid index")


def delete_transactions_by_date(date):
    global data
    data = data[data["date"] != date].reset_index(drop=True)
    data.to_csv(PATH, index=False)


def clear_all_transactions():
    global data
    data = pd.DataFrame(columns=data.columns)
    data.to_csv(PATH, index=False)

def update_transaction(index, date=None, amount=None, type=None, category=None, description=None, Currency=None):
    global data
    if 0 <= index < len(data):
        if date is not None:
            data.at[index, "date"] = date
        if amount is not None:
            data.at[index, "amount"] = amount
        if type is not None:
            data.at[index, "type"] = type
        if category is not None:
            data.at[index, "category"] = category
        if description is not None:
            data.at[index, "description"] = description
        if Currency is not None:
            data.at[index, "Currency"] = Currency
        data.to_csv(PATH, index=False)
    else:
        print("Invalid index")





def get_transactions_by_date(date):
    transactions = data[data["date"] == date]
    return transactions

def get_transactions_by_type(type):
    transactions = data[data["type"] == type]
    return transactions

def get_transactions_by_category(category):
    transactions = data[data["category"] == category]
    return transactions

def get_all_transactions():
    return data


def sort_transactions_by_date(ascending=True):
    global data
    data = data.sort_values(by="date", ascending=ascending).reset_index(drop=True)
    data.to_csv(PATH, index=False)

def sort_transactions_by_amount(ascending=True):
    global data
    data = data.sort_values(by="amount", ascending=ascending).reset_index(drop=True)
    data.to_csv(PATH, index=False)

def sort_transactions_by_category():
    global data
    data = data.sort_values(by="category").reset_index(drop=True)
    data.to_csv(PATH, index=False)

def sort_transactions_by_type():
    global data
    data = data.sort_values(by="type").reset_index(drop=True)
    data.to_csv(PATH, index=False)

def design_report():
    expenses_by_category = data[data["type"] == "expense"].groupby("category")["amount"].sum()
    income_by_category = data[data["type"] == "income"].groupby("category")["amount"].sum()
    total_expenses = get_total_expenses()
    total_income = get_total_income()
    balance = get_balance()

    report = f"--- Financial Report ---\n\n"
    report += f"Total Income: {total_income}\n"
    report += f"Total Expenses: {total_expenses}\n"
    report += f"Balance: {balance}\n\n"
    report += "Income by Category:\n"
    for category, amount in income_by_category.items():
        report += f"  {category}: {amount}\n"
    report += "\nExpenses by Category:\n"
    for category, amount in expenses_by_category.items():
        report += f"  {category}: {amount}\n"

    return report
def export_report_to_pdf(filename="financial_report.pdf", logo_path="logo.png"):
    data = get_all_transactions()  # DataFrame avec colonnes date, amount, type, category, description, Currency
    
    total_income = get_total_income()
    total_expenses = get_total_expenses()
    balance = get_balance()
    
    income_by_category = data[data["type"]=="income"].groupby("category")["amount"].sum()
    expenses_by_category = data[data["type"]=="expense"].groupby("category")["amount"].sum()
    
    pdf = FPDF('P','mm','A4')
    pdf.add_page()
    
    # --- Logo ---
    if logo_path:
        pdf.image(logo_path, x=10, y=8, w=30)
    
    pdf.set_font("Arial","B",16)
    pdf.cell(0, 10, "--- Financial Report ---", ln=True, align="C")
    pdf.ln(10)
    
    # --- Summary ---
    pdf.set_font("Arial","B",12)
    pdf.cell(50,8,"Total Income:", border=0)
    pdf.set_font("Arial","",12)
    pdf.cell(0,8,f"{total_income:.2f} MAD", ln=True)
    
    pdf.set_font("Arial","B",12)
    pdf.cell(50,8,"Total Expenses:", border=0)
    pdf.set_font("Arial","",12)
    pdf.cell(0,8,f"{total_expenses:.2f} MAD", ln=True)
    
    pdf.set_font("Arial","B",12)
    pdf.cell(50,8,"Balance:", border=0)
    pdf.set_font("Arial","",12)
    pdf.cell(0,8,f"{balance:.2f} MAD", ln=True)
    
    pdf.ln(10)
    
    # --- Income by Category ---
    pdf.set_font("Arial","B",14)
    pdf.cell(0,8,"Income by Category:", ln=True)
    pdf.set_font("Arial","",12)
    for cat, amt in income_by_category.items():
        pdf.cell(0,8,f"  {cat}: {amt:.2f} MAD", ln=True)
    
    pdf.ln(5)
    
    # --- Expenses by Category ---
    pdf.set_font("Arial","B",14)
    pdf.cell(0,8,"Expenses by Category:", ln=True)
    pdf.set_font("Arial","",12)
    for cat, amt in expenses_by_category.items():
        pdf.cell(0,8,f"  {cat}: {amt:.2f} MAD", ln=True)
    
    pdf.ln(10)
    
    # --- Full Transactions Table ---
    pdf.set_font("Arial","B",12)
    th = 8  # hauteur ligne
    cols = ["Date","Type","Category","Description","Amount","Currency"]
    col_widths = [25,20,35,60,25,20]
    
    for i, col in enumerate(cols):
        pdf.cell(col_widths[i], th, col, border=1, align="C")
    pdf.ln(th)
    
    pdf.set_font("Arial","",11)
    for _, row in data.iterrows():
        pdf.cell(col_widths[0], th, str(row["date"]), border=1)
        pdf.cell(col_widths[1], th, str(row["type"]), border=1, align="C")
        pdf.cell(col_widths[2], th, str(row["category"]), border=1)
        pdf.cell(col_widths[3], th, str(row["description"]), border=1)
        pdf.cell(col_widths[4], th, f"{row['amount']:.2f}", border=1, align="R")
        pdf.cell(col_widths[5], th, str(row.get("Currency","MAD")), border=1, align="C")
        pdf.ln(th)
    
    pdf.output(filename)


def get_statistics():
    stats = {
        "total_income": get_total_income(),
        "total_expenses": get_total_expenses(),
        "balance": get_balance(),
        "average_income": data[data["type"]=="income"]["amount"].mean(),
        "average_expense": data[data["type"]=="expense"]["amount"].mean(),
        "max_income": data[data["type"]=="income"]["amount"].max(),
        "max_expense": data[data["type"]=="expense"]["amount"].max(),
        "min_income": data[data["type"]=="income"]["amount"].min(),
        "min_expense": data[data["type"]=="expense"]["amount"].min(),
    }
    return stats


def add_recurring_transaction(start_date, amount, type, category, description, months=12):
    from datetime import datetime
    from dateutil.relativedelta import relativedelta

    date = pd.to_datetime(start_date)
    for _ in range(months):
        add_transaction(date.strftime("%Y-%m-%d"), amount, type, category, description)
        date += relativedelta(months=1)

def get_transactions_by_date_range(start_date, end_date):
    mask = (data["date"] >= start_date) & (data["date"] <= end_date)
    return data.loc[mask]



def monthly_summary():
    data['month'] = pd.to_datetime(data['date']).dt.to_period('M')
    summary = data.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
    summary['balance'] = summary.get('income',0) - summary.get('expense',0)
    return summary


def search_transactions(keyword):
    return data[data['description'].str.contains(keyword, case=False, na=False)]



#print(get_expenses_by_category("Food"))
#print(get_income_by_category("Salary"))    
#print(get_total_expenses())
#print(get_total_income())
#print(get_balance())
#add_transaction("2023-10-10", 150, "expense", "entertainment", "Movie night")
#print(get_transactions_by_date("2025-08-07"))
#print(get_transactions_by_type("income"))
#print(get_transactions_by_category("Food"))
#print(get_all_transactions())

