from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 16)
        self.cell(0, 10, "Entrega Inicial - Bootcamp", align="C")
        self.ln(20)

pdf = PDF()
pdf.add_page()
pdf.set_font("helvetica", size=12)

# Informações Pessoais
info = [
    "Nome: Gabriela Yasmin Conceição Viana | RA: 22505273",
    "Professor: Dr. Romes Heriberto",
    "Disciplina: Bootcamp",
    "Curso: Engenharia de Software",
]

for linha in info:
    pdf.cell(0, 10, txt=linha, ln=1)

pdf.ln(10)

# Informações do Projeto
pdf.set_font("helvetica", "B", 14)
pdf.cell(0, 10, txt="Informações do Projeto", ln=1)
pdf.set_font("helvetica", size=12)

pdf.set_font("helvetica", "B", 12)
pdf.cell(35, 10, txt="Nome do projeto: ")
pdf.set_font("helvetica", size=12)
pdf.cell(0, 10, txt="MindStep Tracker", ln=1)

pdf.set_font("helvetica", "B", 12)
pdf.cell(85, 10, txt="Link do repositório público no GitHub: ")
pdf.set_font("helvetica", "U", 12)
pdf.set_text_color(0, 0, 255)
pdf.cell(0, 10, txt="https://github.com/gabrielay-ctrl/estudo", ln=1, link="https://github.com/gabrielay-ctrl/estudo")

pdf.set_text_color(0, 0, 0)
pdf.set_font("helvetica", "B", 12)
pdf.cell(0, 10, txt="Breve descrição da proposta:", ln=1)
pdf.set_font("helvetica", size=12)

resumo = (
    "O MindStep Tracker é uma aplicação de linha de comando (CLI) voltada para auxiliar pessoas neurodivergentes "
    "(como portadores de TDAH e ansiedade crônica) que sofrem com paralisia de tarefas e esquecimento de "
    "autocuidado básico.\n\nO sistema resolve isso forçando a divisão de grandes atividades cotidianas "
    "em no mínimo 3 \"micro-passos\" antes de sua execução, proporcionando acompanhamento guiado e "
    "micro-recompensas para evitar a sobrecarga cognitiva e garantir o progresso passo a passo."
)

pdf.multi_cell(0, 8, txt=resumo)

# Salvar o arquivo
file_path = r"C:\Users\gabit\OneDrive\Área de Trabalho\Entrega_Bootcamp_Gabriela.pdf"
try:
    pdf.output(file_path)
    print(f"PDF gerado com sucesso em: {file_path}")
except Exception:
    alt_path = r"C:\Users\gabit\.gemini\antigravity\scratch\estudo\Entrega_Bootcamp_Gabriela.pdf"
    pdf.output(alt_path)
    print(f"Salvo no caminho alternativo: {alt_path}")
