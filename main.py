import fitz  # PyMuPDF
import re
import csv

# Caminho do PDF
pdf_path = "producaoMedicaDetalhadoJULHO.pdf"
output_csv = "beneficiarios_codigos_completo_julho.csv"

# Abrir o PDF
doc = fitz.open(pdf_path)
pages = [page.get_text("blocks") for page in doc]
doc.close()

# Processar linhas
records = []
current_beneficiary = None
current_date = None

# Loop nas linhas do PDF
for i, page in enumerate(pages):

    for j, line in enumerate(page):
        # Buscar linhas com data + nome do beneficiário (linha principal)
        main_match = re.search(r'(\d{2}/\d{2}/\d{4}) \d{2}:\d{2}:\d{2}\s+\S+\s+\d\s+([A-Z\s]+)\s+\d+,\d{2}', line[4])
        if main_match:
            current_date = main_match.group(1)
            current_beneficiary = main_match.group(2).strip()
            continue

        # Buscar códigos de serviço nas linhas seguintes
        code_match = re.match(r'^(5\d{6})\s', line[4])
        if code_match and current_beneficiary and current_date:
            records.append((current_beneficiary, current_date, code_match.group(1)))

# Salvar CSV
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["beneficiario", "data", "codigo_servico"])
    writer.writerows(records)

print(f"CSV gerado com {len(records)} registros: {output_csv}")
