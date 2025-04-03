import os, uuid, requests
from fpdf import FPDF
from datetime import datetime

# URL da API externa (substitua pela API real)
API_URL = "https://exemplo.com/api/dados"

# Realiza a requisição GET
response = requests.get(url, headers=headers)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    dados = response.json()
else:
    print("Erro ao buscar os dados:", response.status_code)
    exit()


# Geração do layout em pdf
start_time = time.time()

now = datetime.now()

diretorio_saida = f"relatorios_{now.strftime('%Y%m%d')}"
arquivo_log = f"{diretorio_saida}/log_execucao.txt"
    
if not os.path.isdir(diretorio_saida):
    os.mkdir(diretorio_saida)    

logfile = open(arquivo_log, "a", encoding='utf-8')

def parse_date(date_str):
    try:
        # Tenta converter a data com milissegundos
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        # Se falhar, converte sem milissegundos
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")


def gera_arquivo_pdf(dados, diretorio_saida):

    # Verifica se 'dados' é uma lista
    if isinstance(dados, list):

        TABLE_DATA = [
            ("Nr. Atendimento", 
            "Nr. Protocolo", 
            "Nr. Ouvidoria", 
            "Área Atendimento",
            "Observação Abertura",
            "Descr. Atendimento", 
            "Filial", 
            "Usuario", 
            "Data Abertura", 
            "Data Fechamento", 
            "Data Ouvidoria")
    ]
        
    for item in dados:
        dataAbertura = parse_date(item.get('dataAbertura', 'N/A'))
        dataResolucao = parse_date(item.get('dataResolucao', 'N/A'))
        dataOuvidoria = parse_date(item.get('dataOuvidoria', 'N/A'))
        formattedDataAbertura = dataAbertura.strftime("%d/%m/%Y %H:%M:%S")
        formattedDataResolucao = ("" if item.get('statusAtendimento') == 1 | 0 else dataResolucao.strftime("%d/%m/%Y %H:%M:%S"))
        formattedDataOuvidoria = ("" if dataOuvidoria.year == 1 or item.get('statusAtendimento') == 1 | 0 else dataOuvidoria.strftime("%d/%m/%Y %H:%M:%S"))
        cpf = item.get('cpf', 'N/A')

        if(item.get('codigoFilial') == 1):
            filial = "MATRIZ"
        elif(item.get('codigoFilial') == 673):
            filial = "CALL CENTER - ATENTO"
        else:
            filial = ""

        TABLE_DATA.append((
            f"{str(item.get('numeroAtendimento', 'N/A'))}", 
            f"{str(item.get('protocolo', 'N/A'))}", 
            f"{str(item.get('numeroAtendimento', 'N/A'))}", 
            f"{str(item.get('descricaoArea', 'N/A'))}",
            f"{str(item.get('observacaoAbertura', 'N/A'))}",
            f"{str(item.get('descricaoFila', 'N/A'))}",
            f"{filial}",
            f"{str(item.get('nome', 'N/A'))}",
            f"{formattedDataAbertura}",
            f"{formattedDataResolucao}",
            f"{formattedDataOuvidoria}"
        ))

    # Criando o PDF
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("helvetica", "", 12)
    pdf.image('logo_pan_spa.png', x=10, y=10, w=pdf.w - 20)
    pdf.ln(25)

    # Titulo do documento
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(270, 10, f"CHAMADOS - CPF: {str(cpf)}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(5)
    pdf.set_font("helvetica", "", 10)
    pdf.set_font("helvetica", "", size=7)

    # Cria a tabela com os headers e columns
    with pdf.table(width=277.0000833333333, col_widths=(35, 30, 30, 50, 140, 50, 35, 35, 30, 30, 30)) as table:
        for data_row in TABLE_DATA:
            row = table.row()
            for datum in data_row:
                row.cell(datum)
    
    caminho_pdf = os.path.join(diretorio_saida, f"relatorio_chamados_{cpf}-{datetime.now().strftime('%d%m%Y')}.pdf")
    pdf.output(caminho_pdf)


try:

    logfile.write(f"INICIO \n")
    logfile.write(f"Diretório de saída criado: {diretorio_saida} \n")
    logfile.write(f"Inicio leitura do dados de entrada: {response.json()} \n")

    retorno = gera_arquivo_pdf(dados, diretorio_saida)

    if retorno == "":
        logfile.write(f"arquivo: {retorno} gerado com sucesso. \n")
    else:
        logfile.write(f"{retorno} \n")

    end_time = time.time()
    execution_time = end_time - start_time
    logfile.write(f"Tempo de execução: {execution_time:.2f} segundos \n")
    logfile.write(f"TERMINO \n\n")
    logfile.close()

except Exception as e:
    print("Erro: ", str(e))
    logfile.write(f"Erro: {str(e)}\n")
 
