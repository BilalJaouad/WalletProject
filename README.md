# WalletProject  

WalletProject is a **Python-based personal finance manager** that helps you track your income, expenses, and balances.  
It also provides **data visualization** and **predictive analysis** for better financial planning.  

---

## 🚀 Features  

- Track income and expenses by category.  
- Visualize monthly income, expenses, and balance.  
- Predict future income, expenses, and balance using linear regression.  
- User-friendly charts and plots for quick insights.  

---

## 📂 Project Structure  

```bash
WalletProject/
│
├── src/                  # Python source code
│   ├── gui.py            # GUI module
│   ├── plot.py           # Plotting and visualization module
│   ├── predic.py         # Prediction module
│   ├── wallet.py         # Core wallet logic
│   └── main.py           # Main entry point of the project
│
├── data/                 # CSV transaction files
│   └── transactions.csv
│
├── venv/                 # Python virtual environment
│
├── .gitignore            # Git ignored files and folders
├── requirements.txt      # Required Python packages
└── README.md             # Project documentation
```

---

## ⚙️ Installation  

1. **Clone the repository**  
```bash
git clone https://github.com/BilalJaouad/WalletProject.git
cd WalletProject
```

2. **(Optional) Create a virtual environment**  
```bash
python -m venv venv
```

3. **Activate the virtual environment**  
- **Windows**:  
```bash
venv\Scripts\activate
```
- **Linux/macOS**:  
```bash
source venv/bin/activate
```

4. **Install dependencies**  
```bash
pip install -r requirements.txt
```

---

## ▶️ Usage  

Simply run the **main.py** file:  

```bash
python src/main.py
```

### 💡 Note  
If you encounter issues running from the terminal, open the project in **VS Code** and run the script directly from the editor to ensure paths and environments are properly recognized.  

---

## 📦 Dependencies  

The project uses the following main libraries (see `requirements.txt` for exact versions):  
- pandas  
- numpy  
- matplotlib  
- seaborn  
- scikit-learn  
- fpdf  
- etc.  

---

## 🤝 Contributing  

Contributions are welcome!  
Feel free to fork the project, make improvements, and submit **pull requests**.  

---

📌 **Author**  
Developed by **Bilal Jaouad**  
📧 bilaljaouad7@gmail.com
