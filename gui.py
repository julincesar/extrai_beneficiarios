
import tkinter as tk
from tkinter import ttk, filedialog
import fitz  # PyMuPDF
import re
import csv

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Extrator de Beneficiários")
        self.root.geometry("800x600")

        self.pdf_path = tk.StringVar()
        self.csv_path = tk.StringVar()
        self.records = []

        # Frame for file selection
        file_frame = ttk.Frame(self.root, padding="10")
        file_frame.pack(fill="x")

        ttk.Label(file_frame, text="Arquivo PDF:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(file_frame, textvariable=self.pdf_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Selecionar PDF", command=self.select_pdf).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(file_frame, text="Arquivo CSV de Saída:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(file_frame, textvariable=self.csv_path, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Selecionar CSV", command=self.select_csv).grid(row=1, column=2, padx=5, pady=5)

        # Frame for buttons
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill="x")

        ttk.Button(button_frame, text="Processar", command=self.process_pdf).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Salvar", command=self.save_csv).pack(side="left", padx=5)

        # Frame for the grid
        grid_frame = ttk.Frame(self.root, padding="10")
        grid_frame.pack(fill="both", expand=True)

        # Scrollbars
        vsb = ttk.Scrollbar(grid_frame, orient="vertical")
        hsb = ttk.Scrollbar(grid_frame, orient="horizontal")

        self.tree = ttk.Treeview(grid_frame, columns=("beneficiario", "data", "codigo_servico"), show="headings",
                                 yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.heading("beneficiario", text="Beneficiário")
        self.tree.heading("data", text="Data")
        self.tree.heading("codigo_servico", text="Código de Serviço")

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

    def select_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if path:
            self.pdf_path.set(path)

    def select_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if path:
            self.csv_path.set(path)

    def process_pdf(self):
        pdf_path = self.pdf_path.get()
        if not pdf_path:
            tk.messagebox.showerror("Erro", "Selecione um arquivo PDF.")
            return

        try:
            doc = fitz.open(pdf_path)
            pages = [page.get_text("blocks") for page in doc]
            doc.close()

            self.records = []
            current_beneficiary = None
            current_date = None

            for i, page in enumerate(pages):
                for j, line in enumerate(page):
                    main_match = re.search(r'(\d{2}/\d{2}/\d{4}) \d{2}:\d{2}:\d{2}\s+\S+\s+\d\s+([A-Z\s]+)\s+\d+,\d{2}', line[4])
                    if main_match:
                        current_date = main_match.group(1)
                        current_beneficiary = main_match.group(2).strip()
                        continue

                    code_match = re.match(r'^(5\d{6})\s', line[4])
                    if code_match and current_beneficiary and current_date:
                        self.records.append((current_beneficiary, current_date, code_match.group(1)))

            # Clear previous data
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Insert new data
            for record in self.records:
                self.tree.insert("", "end", values=record)

            tk.messagebox.showinfo("Sucesso", f"{len(self.records)} registros processados.")

        except Exception as e:
            tk.messagebox.showerror("Erro", f"Ocorreu um erro ao processar o PDF: {e}")

    def save_csv(self):
        csv_path = self.csv_path.get()
        if not csv_path:
            tk.messagebox.showerror("Erro", "Selecione um arquivo CSV de saída.")
            return

        if not self.records:
            tk.messagebox.showwarning("Aviso", "Não há dados para salvar. Processe um PDF primeiro.")
            return

        try:
            with open(csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["beneficiario", "data", "codigo_servico"])
                writer.writerows(self.records)
            tk.messagebox.showinfo("Sucesso", f"CSV gerado com {len(self.records)} registros: {csv_path}")
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o CSV: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
