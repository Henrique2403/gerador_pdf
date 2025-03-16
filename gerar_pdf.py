import os, uuid, requests
from fpdf import FPDF
from datetime import datetime

# URL da API externa (substitua pela API real)
API_URL = "https://exemplo.com/api/dados"

# Realiza a requisição GET
response = requests.get(API_URL)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    data = response.json()
else:
    print("Erro ao buscar os dados:", response.status_code)
    exit()


# Criando o PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", "", 12)

# Título do documento
pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, "COMMERCIAL INVOICE", ln=True, align="C")
pdf.ln(5)

# Informações principais
pdf.set_font("Arial", "B", 12)
pdf.cell(100, 8, "Empresa XYZ", ln=True)
pdf.set_font("Arial", "", 12)
pdf.cell(100, 8, f"Protocolo: {data.get('protocolo', 'N/A')}", ln=True)
pdf.cell(100, 8, f"Data Abertura: {datetime.strptime(data.get('dataAbertura', '2025-03-14T19:00:20.906Z'), '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y')}", ln=True)
pdf.cell(100, 8, f"Email: {data.get('email', 'N/A')}", ln=True)
pdf.cell(100, 8, f"Nome: {data.get('nome', 'N/A')}", ln=True)
pdf.cell(100, 8, f"Telefone: ({data.get('numeroDDD1', 'N/A')}) {data.get('numeroTelefone1', 'N/A')}", ln=True)
pdf.ln(10)

# Tabela com os detalhes do atendimento
pdf.set_font("Arial", "B", 12)
pdf.cell(190, 8, "Detalhes do Atendimento", ln=True, align="C")
pdf.ln(5)

pdf.set_font("Arial", "B", 10)
pdf.cell(50, 8, "Campo", 1)
pdf.cell(140, 8, "Detalhe", 1, ln=True)

pdf.set_font("Arial", "", 10)
campos = [
    ("Status Atendimento", data.get("statusAtendimento", "N/A")),
    ("Data Resolucao", datetime.strptime(data.get("dataResolucao", "2025-03-14T19:00:20.906Z"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d/%m/%Y")),
    ("Código Fechamento", data.get("codigoFechamento", "N/A")),
    ("Descrição Produto", data.get("descricaoProduto", "N/A")),
    ("Observação Abertura", data.get("observacaoAbertura", "N/A")),
    ("Observação Fechamento", data.get("observacaoFechamento", "N/A")),
]

for campo, valor in campos:
    pdf.cell(50, 8, campo, 1)
    pdf.cell(140, 8, str(valor), 1, ln=True)

pdf.ln(10)


# Criar a pasta 'gerador_pdf' se não existir
output_dir = f"relatorio{datetime.now().strftime("%Y-%m-%d")}"
os.makedirs(output_dir, exist_ok=True)

# Criar guid para nomear arquivo pdf
guid = uuid.uuid4()

# Caminho do PDF corrigido
pdf_path = os.path.join(output_dir, f"{guid}{datetime.now().strftime("%Y-%m-%d")}.pdf")
pdf.output(pdf_path)

print(f"PDF gerado com sucesso: {pdf_path}")
