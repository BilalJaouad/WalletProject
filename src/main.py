import tkinter as tk
from gui import WalletGUI

def main():
    root = tk.Tk()
    app = WalletGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
