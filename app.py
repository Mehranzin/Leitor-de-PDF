import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageFilter
import pytesseract
import pdfplumber
from openpyxl import Workbook, load_workbook
from datetime import datetime

# Configuração do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# === PRÉ-PROCESSAMENTO ===
def preprocessar_imagem(caminho: str) -> Image.Image:
    imagem = Image.open(caminho).convert("L")
    imagem = imagem.filter(ImageFilter.SHARPEN)
    imagem = imagem.point(lambda x: 0 if x < 140 else 255)
    return imagem

# === EXTRAÇÃO DE TEXTO ===
def extrair_texto(caminho: str) -> str:
    texto_extraido = ""
    if caminho.lower().endswith(".pdf"):
        with pdfplumber.open(caminho) as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()
                if texto:
                    texto_extraido += texto + "\n"
                else:
                    imagem = pagina.to_image(resolution=300).original
                    texto_extraido += pytesseract.image_to_string(imagem, lang="por+eng", config="--psm 6") + "\n"
    elif caminho.lower().endswith((".png", ".jpg", ".jpeg")):
        imagem = preprocessar_imagem(caminho)
        texto_extraido = pytesseract.image_to_string(imagem, lang="por+eng", config="--psm 6")
    else:
        raise ValueError("Formato não suportado. Use PDF ou imagem.")
    return texto_extraido.strip()

# === EXTRAÇÃO DE DADOS DO TEXTO ===
def extrair_dados(texto: str) -> dict:
    cliente_match = re.search(r"(?i)cliente[:\s]*([^\n]+)", texto)
    cliente = cliente_match.group(1).strip() if cliente_match else "Não encontrado"

    vencimento_match = re.search(r"\b(\d{2}[/-]\d{2}[/-]\d{4})\b", texto)
    vencimento = vencimento_match.group(1) if vencimento_match else "Não encontrado"

    valor_match = re.search(r"(?i)(valor\s*(do\s*)?documento)[^\d]*(\d{1,3}(?:\.\d{3})*,\d{2})", texto)
    if valor_match:
        valor = valor_match.group(3)
    else:
        valores = re.findall(r"\d{1,3}(?:\.\d{3})*,\d{2}", texto)
        valores_float = [float(v.replace('.', '').replace(',', '.')) for v in valores]
        valor_maior = max(valores_float, default=None)
        valor = f"{valor_maior:,.2f}".replace('.', ',') if valor_maior else "Não encontrado"

    cpf_cnpj_match = re.search(r"\b(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})\b", texto)
    cpf_cnpj = cpf_cnpj_match.group(1) if cpf_cnpj_match else "Não encontrado"

    return {
        "Cliente": cliente,
        "Vencimento": vencimento,
        "Valor": f"R$ {valor}" if valor != "Não encontrado" else valor,
        "CPF/CNPJ": cpf_cnpj
    }

# === INTERFACE (GUI) ===
def selecionar_arquivo(caminho=None):
    if not caminho:
        caminho = filedialog.askopenfilename(
            title="Selecionar ou arrastar Arquivo",
            filetypes=[("PDF e Imagens", "*.pdf *.png *.jpg *.jpeg")]
        )
    if not caminho:
        return

    btn_arquivo.config(text="⏳ Processando...", state="disabled")
    janela.update_idletasks()

    try:
        texto = extrair_texto(caminho)
        dados = extrair_dados(texto)

        texto_area.config(state='normal')
        texto_area.delete(1.0, tk.END)
        texto_area.insert(tk.END, texto)
        texto_area.config(state='disabled')

        cliente_var.set(dados["Cliente"])
        vencimento_var.set(dados["Vencimento"])
        valor_var.set(dados["Valor"])
        doc_var.set(dados["CPF/CNPJ"])

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar o arquivo:\n{e}")

    btn_arquivo.config(text="📂 Selecionar ou arrastar Arquivo", state="normal")

# === MODO ESCURO ===
def alternar_tema():
    if janela["bg"] == "#1e1e1e":
        aplicar_tema_claro()
    else:
        aplicar_tema_escuro()

def aplicar_tema_escuro():
    janela.config(bg="#1e1e1e")
    texto_frame.config(bg="#1e1e1e", fg="white")
    frame_dados.config(bg="#1e1e1e", fg="white")
    rodape.config(bg="#1e1e1e", fg="gray")
    for child in frame_dados.winfo_children():
        if isinstance(child, tk.Label):
            child.config(bg="#1e1e1e", fg="white")

def aplicar_tema_claro():
    janela.config(bg="#f9f9f9")
    texto_frame.config(bg="#f9f9f9", fg="black")
    frame_dados.config(bg="#f9f9f9", fg="black")
    rodape.config(bg="#f9f9f9", fg="gray")
    for child in frame_dados.winfo_children():
        if isinstance(child, tk.Label):
            child.config(bg="#f9f9f9", fg="black")

# === JANELA PRINCIPAL ===
janela = TkinterDnD.Tk()
janela.title(" Leitor de PDFs e Boletos")
largura_janela = 900
altura_janela = 720
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
pos_x = (largura_tela // 2) - (largura_janela // 2)
pos_y = (altura_tela // 2) - (altura_janela // 2)
janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
janela.configure(bg="#f9f9f9")
janela.resizable(False, False)

# Estilo
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 11), padding=10, background="#1900FF", foreground="white")
style.map("TButton", background=[("active", "#3e30b6")])

# Botão e tema
top_frame = tk.Frame(janela, bg="#f9f9f9")
top_frame.pack(fill=tk.X, padx=10, pady=10)
btn_arquivo = ttk.Button(top_frame, text="📂 Selecionar ou arrastar Arquivo", command=lambda: selecionar_arquivo())
btn_arquivo.pack(side=tk.LEFT)
btn_tema = ttk.Button(top_frame, text="Tema", command=alternar_tema)
btn_tema.pack(side=tk.RIGHT, padx=5)

# Área de texto
texto_frame = tk.LabelFrame(janela, text="📝 Texto Extraído", font=("Segoe UI", 10, "bold"), bg="#f9f9f9")
texto_frame.pack(padx=10, pady=10, fill="both")
texto_area = scrolledtext.ScrolledText(texto_frame, wrap=tk.WORD, width=100, height=20, font=("Courier New", 10), bg="white")
texto_area.pack(padx=10, pady=5)
texto_area.config(state='disabled')

# Dados extraídos
frame_dados = tk.LabelFrame(janela, text="📌 Dados Identificados", font=("Segoe UI", 10, "bold"), bg="#f9f9f9")
frame_dados.pack(padx=10, pady=15, fill="x")

cliente_var = tk.StringVar()
vencimento_var = tk.StringVar()
valor_var = tk.StringVar()
doc_var = tk.StringVar()

def criar_linha(label, var, row, emoji):
    tk.Label(frame_dados, text=f"{emoji} {label}:", font=("Segoe UI", 10, "bold"), bg="#f9f9f9").grid(row=row, column=0, sticky="w", padx=10, pady=5)
    ttk.Entry(frame_dados, textvariable=var, width=60, font=("Segoe UI", 10)).grid(row=row, column=1, padx=5, pady=5)

criar_linha("Cliente", cliente_var, 0, "👤")
criar_linha("Vencimento", vencimento_var, 1, "📅")
criar_linha("Valor", valor_var, 2, "💰")
criar_linha("CPF/CNPJ", doc_var, 3, "🧾")

# Rodapé
rodape = tk.Label(janela, text="Mehran Productions® • v1.4", font=("Segoe UI", 9), fg="gray", bg="#f9f9f9")
rodape.pack(pady=10)

# Suporte a arrastar e soltar
janela.drop_target_register(DND_FILES)
janela.dnd_bind("<<Drop>>", lambda e: selecionar_arquivo(e.data.strip('{}')))

janela.mainloop()
