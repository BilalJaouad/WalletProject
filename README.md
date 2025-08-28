# WalletProject

WalletProject is a Python-based personal finance manager that allows you to track your income, expenses, and balances. It provides data visualization and predictive analysis for better financial planning.

## Features

- Track income and expenses by category.
- Visualize monthly income, expenses, and balance.
- Predict future income, expenses, and balance using linear regression.
- User-friendly plots and charts for quick insights.

## Project Structure

```
WalletProject/
│
├── src/                  # Python source code
│   ├── gui.py            # GUI module
│   ├── plot.py           # Plotting and visualization module
│   ├── predic.py         # Prediction module
│   └── wallet.py         # Core wallet logic
│
├── data/                 # CSV files for transactions
│   └── transactions.csv
│
├── venv/                 # Python virtual environment
├── .gitignore            # Files and folders ignored by git
├── requirements.txt      # Required Python packages
└── README.md             # Project documentation
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/BilalJaouad/WalletProject.git
cd WalletProject
```

2. (Optional) Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

* **Windows**:

```bash
venv\Scripts\activate
```

* **Linux/macOS**:

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

You can run the project by executing the main scripts in the `src` folder. Example:

```bash
python src/gui.py
```

### Note

In case of any issues running the code from the terminal, **open the project in VS Code** and run the scripts directly from the editor. This ensures that all paths and environments are correctly recognized.

## Dependencies

The project requires the following Python libraries (see `requirements.txt` for exact versions):

* pandas
* numpy
* matplotlib
* seaborn
* scikit-learn
* fpdf
* etc.

## Contributing

Feel free to fork the project, make improvements, and submit pull requests.



📌 Author

Developed by Bilal Jaouad