import fitz  # PyMuPDF
import re
import csv

pdf_path = "producaoMedicaDetalhadoNovo.pdf"
output_csv = "beneficiarios_codigos_completo_novo.csv"

doc = fitz.open(pdf_path)

records = []
current_beneficiary = None
current_date = None

for page in doc:
    blocks = page.get_text("blocks")

    # Ordenar blocos de cima pra baixo, esquerda pra direita
    blocks = sorted(blocks, key=lambda b: (round(b[1]), round(b[0])))

    for b in blocks:
        text = b[4].strip()

        # Normalizar espaços
        text = re.sub(r'\s+', ' ', text)

        # =========================
        # 1. LINHA PRINCIPAL
        # =========================
        # Exemplo esperado:
        # 20014 ... 02/07/2025 12:05:47 ... NOME DO BENEFICIARIO ... 120,00

        main_match = re.search(
            r'(\d{2}/\d{2}/\d{4})\s+\d{2}:\d{2}:\d{2}.*?([A-ZÁÉÍÓÚÃÕÇ\s]+?)\s+\d+,\d{2}',
            text
        )

        if main_match:
            current_date = main_match.group(1)
            current_beneficiary = main_match.group(2).strip()
            continue

        # =========================
        # 2. LINHAS DE SERVIÇO
        # =========================
        # Captura QUALQUER código começando com 5xxxxxx
        codes = re.findall(r'\b(5\d{6})\b', text)

        if codes and current_beneficiary and current_date:
            for code in codes:
                records.append((current_beneficiary, current_date, code))

doc.close()

# =========================
# 3. SALVAR CSV
# =========================
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["beneficiario", "data", "codigo_servico"])
    writer.writerows(records)

print(f"CSV gerado com {len(records)} registros: {output_csv}")