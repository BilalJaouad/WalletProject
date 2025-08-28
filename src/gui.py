import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import pandas as pd
import wallet    # ton module principal (anciennement transactions)
import plot      # module plots (retourne Figures)
import predic    # module de prédiction

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
    _HAS_TOOLBAR = True
except Exception:
    _HAS_TOOLBAR = False


class WalletGUI:
    def __init__(self, root):
        self.root = root
        root.title("Wallet Manager")
        root.geometry("1200x700")

        # --------------------------
        # Contrôles supérieurs
        # --------------------------
        ctrl_frame = ttk.Frame(root, padding=(10, 8))
        ctrl_frame.pack(fill="x", side="top")

        ttk.Label(ctrl_frame, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=4, pady=4)
        self.entry_date = ttk.Entry(ctrl_frame, width=12); self.entry_date.grid(row=0, column=1, padx=4)

        ttk.Label(ctrl_frame, text="Montant").grid(row=0, column=2, padx=4)
        self.entry_amount = ttk.Entry(ctrl_frame, width=12); self.entry_amount.grid(row=0, column=3, padx=4)

        ttk.Label(ctrl_frame, text="Type").grid(row=0, column=4, padx=4)
        self.combo_type = ttk.Combobox(ctrl_frame, values=["income", "expense"], width=10, state="readonly")
        self.combo_type.grid(row=0, column=5, padx=4); self.combo_type.set("expense")

        ttk.Label(ctrl_frame, text="Catégorie").grid(row=0, column=6, padx=4)
        self.entry_category = ttk.Entry(ctrl_frame, width=15); self.entry_category.grid(row=0, column=7, padx=4)

        ttk.Label(ctrl_frame, text="Description").grid(row=0, column=8, padx=4)
        self.entry_description = ttk.Entry(ctrl_frame, width=20); self.entry_description.grid(row=0, column=9, padx=4)

        ttk.Button(ctrl_frame, text="Ajouter", command=self.add_transaction).grid(row=0, column=10, padx=6)

        # Recherche et filtrage
        ttk.Label(ctrl_frame, text="Recherche (description)").grid(row=1, column=0, padx=4, pady=6)
        self.entry_search = ttk.Entry(ctrl_frame, width=30); self.entry_search.grid(row=1, column=1, columnspan=3, sticky="w", padx=4)
        ttk.Button(ctrl_frame, text="Rechercher", command=self.search_transactions).grid(row=1, column=4, padx=4)

        ttk.Label(ctrl_frame, text="Début").grid(row=1, column=5, padx=2)
        self.entry_start = ttk.Entry(ctrl_frame, width=12); self.entry_start.grid(row=1, column=6, padx=2)
        ttk.Label(ctrl_frame, text="Fin").grid(row=1, column=7, padx=2)
        self.entry_end = ttk.Entry(ctrl_frame, width=12); self.entry_end.grid(row=1, column=8, padx=2)
        ttk.Button(ctrl_frame, text="Filtrer date", command=self.filter_by_date).grid(row=1, column=9, padx=4)

        ttk.Button(ctrl_frame, text="Supprimer sélection", command=self.delete_selected).grid(row=1, column=10, padx=4)
        ttk.Button(ctrl_frame, text="Modifier sélection", command=self.edit_selected).grid(row=1, column=11, padx=4)

        # --------------------------
        # Frame central : Treeview + plots
        # --------------------------
        mid_frame = ttk.Frame(root, padding=(6,6))
        mid_frame.pack(fill="both", expand=True)

        columns = ("index", "date", "amount", "type", "category", "description", "Currency")
        self.tree = ttk.Treeview(mid_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("index", text="#"); self.tree.column("index", width=50, anchor="center")
        self.tree.heading("date", text="Date"); self.tree.column("date", width=100, anchor="center")
        self.tree.heading("amount", text="Montant"); self.tree.column("amount", width=100, anchor="e")
        self.tree.heading("type", text="Type"); self.tree.column("type", width=80, anchor="center")
        self.tree.heading("category", text="Catégorie"); self.tree.column("category", width=140, anchor="w")
        self.tree.heading("description", text="Description"); self.tree.column("description", width=340, anchor="w")
        self.tree.heading("Currency", text="Devise"); self.tree.column("Currency", width=60, anchor="center")

        vsb = ttk.Scrollbar(mid_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(mid_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.columnconfigure(0, weight=1)

        # Frame plots à droite
        plots_frame = ttk.Frame(mid_frame, padding=(8,8))
        plots_frame.grid(row=0, column=2, sticky="ns", padx=8)

        ttk.Label(plots_frame, text="Plots", font=("TkDefaultFont", 10, "bold")).pack(pady=(2,6))
        # Graphiques réels
        ttk.Button(plots_frame, text="Expenses by Category", width=28, command=lambda: self.open_plot(plot.plot_expenses_by_category_fig)).pack(pady=4)
        ttk.Button(plots_frame, text="Income by Category", width=28, command=lambda: self.open_plot(plot.plot_income_by_category_fig)).pack(pady=4)
        ttk.Button(plots_frame, text="Monthly Balance", width=28, command=lambda: self.open_plot(plot.plot_monthly_balance_fig)).pack(pady=4)
        ttk.Button(plots_frame, text="Income vs Expenses (monthly)", width=28, command=lambda: self.open_plot(plot.plot_income_vs_expenses_monthly_fig)).pack(pady=4)

        # Prédictions ML
        ttk.Label(plots_frame, text="Prédictions ML", font=("TkDefaultFont", 10, "bold")).pack(pady=(12,6))
        ttk.Button(plots_frame, text="Predict Next Month Income", width=28, command=self.plot_predict_income).pack(pady=4)
        ttk.Button(plots_frame, text="Predict Next Month Expense", width=28, command=self.plot_predict_expense).pack(pady=4)
        ttk.Button(plots_frame, text="Predict Next Month Balance", width=28, command=self.plot_predict_balance).pack(pady=4)

        # --------------------------
        # Bottom
        # --------------------------
        bottom_buttons = ttk.Frame(root, padding=(10,5))
        bottom_buttons.pack(fill="x", side="bottom")
        ttk.Button(bottom_buttons, text="Exporter PDF", command=self.export_pdf).pack(side="left", padx=6)
        ttk.Button(bottom_buttons, text="Statistiques", command=self.show_statistics).pack(side="left", padx=6)
        ttk.Button(bottom_buttons, text="Rafraîchir", command=self.load_transactions).pack(side="left", padx=6)
        ttk.Button(bottom_buttons, text="Tout effacer (CSV)", command=self.clear_all).pack(side="right", padx=6)

        # Charger les transactions initiales
        self.load_transactions()

    # --------------------------
    # CRUD / affichage / filtres
    # --------------------------
    def load_transactions(self, df=None):
        """Charge les transactions (par défaut toutes) dans le Treeview.
        Utilise des indices positionnels 0..n-1 pour les opérations (safe)."""
        for i in self.tree.get_children():
            self.tree.delete(i)

        if df is None:
            df = wallet.get_all_transactions().copy()

        # créer un index positionnel sûr pour usage dans le treeview
        df_display = df.reset_index(drop=True).reset_index()  # colonne 'index' = position 0..n-1
        for _, row in df_display.iterrows():
            iid = str(int(row["index"]))
            values = (int(row["index"]),
                      row.get("date", ""),
                      row.get("amount", ""),
                      row.get("type", ""),
                      row.get("category", ""),
                      row.get("description", ""),
                      row.get("Currency", "MAD"))
            self.tree.insert("", "end", iid=iid, values=values)

    def validate_entries(self, date_str, amount_str, txn_type):
        # Date format
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Erreur", "Format de date invalide. Utiliser YYYY-MM-DD.")
            return False
        # Amount numeric > 0
        try:
            amt = float(amount_str)
            if amt <= 0:
                messagebox.showerror("Erreur", "Le montant doit être positif.")
                return False
        except Exception:
            messagebox.showerror("Erreur", "Montant invalide.")
            return False
        # Type
        if txn_type not in ("income", "expense"):
            messagebox.showerror("Erreur", "Type doit être 'income' ou 'expense'.")
            return False
        return True

    def add_transaction(self):
        date = self.entry_date.get().strip()
        amount = self.entry_amount.get().strip()
        txn_type = self.combo_type.get().strip()
        category = self.entry_category.get().strip() or "Other"
        description = self.entry_description.get().strip() or ""

        if not self.validate_entries(date, amount, txn_type):
            return

        try:
            wallet.add_transaction(date, float(amount), txn_type, category, description)
            messagebox.showinfo("OK", "Transaction ajoutée.")
            # vider champs
            self.entry_date.delete(0, "end")
            self.entry_amount.delete(0, "end")
            self.entry_category.delete(0, "end")
            self.entry_description.delete(0, "end")
            self.load_transactions()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ajouter : {e}")

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Info", "Aucune ligne sélectionnée.")
            return
        idx = int(sel[0])  # position index
        confirm = messagebox.askyesno("Confirmer", f"Supprimer la transaction #{idx} ?")
        if not confirm:
            return
        try:
            wallet.delete_transaction(idx)
            messagebox.showinfo("OK", "Transaction supprimée.")
            self.load_transactions()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de supprimer : {e}")

    def edit_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Info", "Aucune ligne sélectionnée.")
            return
        idx = int(sel[0])  # position index
        df = wallet.get_all_transactions().reset_index(drop=True)
        if idx < 0 or idx >= len(df):
            messagebox.showerror("Erreur", "Index invalide.")
            return
        row = df.loc[idx]

        # Fenêtre de modification simple
        edit = tk.Toplevel(self.root)
        edit.title(f"Modifier #{idx}")
        edit.geometry("420x260")
        ttk.Label(edit, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=8, pady=8)
        e_date = ttk.Entry(edit); e_date.grid(row=0, column=1); e_date.insert(0, row.get("date", ""))

        ttk.Label(edit, text="Montant").grid(row=1, column=0, padx=8, pady=8)
        e_amount = ttk.Entry(edit); e_amount.grid(row=1, column=1); e_amount.insert(0, row.get("amount", ""))

        ttk.Label(edit, text="Type").grid(row=2, column=0, padx=8, pady=8)
        e_type = ttk.Combobox(edit, values=["income", "expense"], state="readonly"); e_type.grid(row=2, column=1)
        e_type.set(row.get("type", "expense"))

        ttk.Label(edit, text="Catégorie").grid(row=3, column=0, padx=8, pady=8)
        e_cat = ttk.Entry(edit); e_cat.grid(row=3, column=1); e_cat.insert(0, row.get("category", ""))

        ttk.Label(edit, text="Description").grid(row=4, column=0, padx=8, pady=8)
        e_desc = ttk.Entry(edit); e_desc.grid(row=4, column=1); e_desc.insert(0, row.get("description", ""))

        ttk.Label(edit, text="Devise").grid(row=5, column=0, padx=8, pady=8)
        e_cur = ttk.Entry(edit); e_cur.grid(row=5, column=1); e_cur.insert(0, row.get("Currency", "MAD"))

        def save_edit():
            new_date = e_date.get().strip()
            new_amount = e_amount.get().strip()
            new_type = e_type.get().strip()
            new_cat = e_cat.get().strip()
            new_desc = e_desc.get().strip()
            new_cur = e_cur.get().strip()

            if not self.validate_entries(new_date, new_amount, new_type):
                return
            try:
                wallet.update_transaction(idx, date=new_date, amount=float(new_amount),
                                          type=new_type, category=new_cat, description=new_desc, Currency=new_cur)
                messagebox.showinfo("OK", "Transaction modifiée.")
                edit.destroy()
                self.load_transactions()
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de modifier : {e}")

        ttk.Button(edit, text="Sauvegarder", command=save_edit).grid(row=6, column=0, columnspan=2, pady=10)

    def export_pdf(self):
        try:
            fname = simpledialog.askstring("Export PDF", "Nom du fichier (ex: report.pdf) :", initialvalue="financial_report.pdf")
            if not fname:
                return
            wallet.export_report_to_pdf(filename=fname)
            messagebox.showinfo("OK", f"PDF généré : {fname}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Export PDF échoué : {e}")

    def show_statistics(self):
        try:
            stats = wallet.get_statistics()
            txt = (
                f"Total Income: {stats.get('total_income',0)}\n"
                f"Total Expenses: {stats.get('total_expenses',0)}\n"
                f"Balance: {stats.get('balance',0)}\n\n"
                f"Moyenne Income: {stats.get('average_income',0):.2f}\n"
                f"Moyenne Expense: {stats.get('average_expense',0):.2f}\n"
                f"Max Income: {stats.get('max_income',0)}\n"
                f"Max Expense: {stats.get('max_expense',0)}\n"
            )
            messagebox.showinfo("Statistiques", txt)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'obtenir statistiques : {e}")

    def search_transactions(self):
        kw = self.entry_search.get().strip()
        if not kw:
            messagebox.showwarning("Info", "Entrez un mot-clé pour la recherche.")
            return
        try:
            res = wallet.search_transactions(kw)
            if res.empty:
                messagebox.showinfo("Résultat", "Aucune transaction trouvée.")
                return
            self.load_transactions(df=res)
        except Exception as e:
            messagebox.showerror("Erreur", f"Recherche échouée : {e}")

    def filter_by_date(self):
        start = self.entry_start.get().strip()
        end = self.entry_end.get().strip()
        if not start or not end:
            messagebox.showwarning("Info", "Entrer une date de début et de fin (YYYY-MM-DD).")
            return
        try:
            res = wallet.get_transactions_by_date_range(start, end)
            if res.empty:
                messagebox.showinfo("Résultat", "Aucune transaction dans cet intervalle.")
                return
            self.load_transactions(df=res)
        except Exception as e:
            messagebox.showerror("Erreur", f"Filtrage échoué : {e}")

    def clear_all(self):
        confirm = messagebox.askyesno("Confirmer", "Effacer toutes les transactions du CSV ? Cette action est irréversible.")
        if not confirm:
            return
        try:
            wallet.clear_all_transactions()
            messagebox.showinfo("OK", "Toutes les transactions ont été effacées.")
            self.load_transactions()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'effacer : {e}")

    # --------------------------
    # Plots embedding
    # --------------------------
    def open_plot(self, fig_func):
        """
        Ouvre un plot matplotlib dans une nouvelle fenêtre.
        fig_func: fonction qui retourne une matplotlib.figure.Figure
        """
        try:
            fig = fig_func()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de générer le plot : {e}")
            return

        win = tk.Toplevel(self.root)
        win.title("Plot")
        win.geometry("900x600")

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        if _HAS_TOOLBAR:
            toolbar = NavigationToolbar2Tk(canvas, win)
            toolbar.update()
            toolbar.pack(side="bottom", fill="x")

        def save_png():
            fname = simpledialog.askstring("Save PNG", "Nom du fichier (ex: plot.png) :", initialvalue="plot.png")
            if not fname:
                return
            try:
                fig.savefig(fname, bbox_inches='tight')
                messagebox.showinfo("OK", f"Image sauvegardée : {fname}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder : {e}")

        btn_frame = ttk.Frame(win, padding=(6,6))
        btn_frame.pack(side="bottom", fill="x")
        ttk.Button(btn_frame, text="Save PNG", command=save_png).pack(side="right", padx=6)

    # --------------------------
    # Prédictions (ML)
    # --------------------------
    def plot_predict_income(self):
        try:
            pred_value = predic.predict_next_month_income()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur prédiction : {e}")
            return

        if pred_value is None:
            messagebox.showinfo("Prédiction", "Pas assez de données pour prédire le revenu.")
            return

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6,4))
        ax.bar(["Next Month Income"], [pred_value], color="#2ca02c")
        ax.set_ylabel("Montant")
        ax.set_title("Prédiction Revenu Prochain Mois")
        for i, v in enumerate([pred_value]):
            ax.text(i, v + 0.01 * max(abs(v), 1), f"{v:.2f}", ha='center', va='bottom')
        self._show_matplotlib_fig(fig)

    def plot_predict_expense(self):
        try:
            pred_value = predic.predict_next_month_expense()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur prédiction : {e}")
            return

        if pred_value is None:
            messagebox.showinfo("Prédiction", "Pas assez de données pour prédire les dépenses.")
            return

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6,4))
        ax.bar(["Next Month Expense"], [pred_value], color="#d62728")
        ax.set_ylabel("Montant")
        ax.set_title("Prédiction Dépenses Prochain Mois")
        for i, v in enumerate([pred_value]):
            ax.text(i, v + 0.01 * max(abs(v), 1), f"{v:.2f}", ha='center', va='bottom')
        self._show_matplotlib_fig(fig)

    def plot_predict_balance(self):
        try:
            pred_value = predic.predict_next_month_balance()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur prédiction : {e}")
            return

        if pred_value is None:
            messagebox.showinfo("Prédiction", "Pas assez de données pour prédire la balance.")
            return

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6,4))
        ax.bar(["Next Month Balance"], [pred_value], color="#1f77b4")
        ax.set_ylabel("Montant")
        ax.set_title("Prédiction Balance Prochain Mois")
        for i, v in enumerate([pred_value]):
            ax.text(i, v + 0.01 * max(abs(v), 1), f"{v:.2f}", ha='center', va='bottom')
        self._show_matplotlib_fig(fig)

    def _show_matplotlib_fig(self, fig):
        """
        Ouvre un plot matplotlib dans une nouvelle fenêtre.
        """
        win = tk.Toplevel(self.root)
        win.title("Plot")
        win.geometry("700x500")
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        if _HAS_TOOLBAR:
            toolbar = NavigationToolbar2Tk(canvas, win)
            toolbar.update()
            toolbar.pack(side="bottom", fill="x")


# Pour debug local rapide uniquement (si tu exécutes gui.py directement)
if __name__ == "__main__":
    root = tk.Tk()
    app = WalletGUI(root)
    root.mainloop()
