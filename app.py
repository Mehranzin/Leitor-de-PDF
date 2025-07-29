import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from PIL import Image, ImageFilter
import pytesseract
import pdfplumber

# Caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocessar_imagem(caminho: str) -> Image.Image:
    imagem = Image.open(caminho).convert("L")
    imagem = imagem.filter(ImageFilter.SHARPEN)
    imagem = imagem.point(lambda x: 0 if x < 140 else 255)
    return imagem

def extrair_texto(caminho: str) -> str:
    if caminho.lower().endswith(".pdf"):
        with pdfplumber.open(caminho) as pdf:
            return "\n".join(pagina.extract_text() or "" for pagina in pdf.pages)
    elif caminho.lower().endswith((".png", ".jpg", ".jpeg")):
        imagem = preprocessar_imagem(caminho)
        return pytesseract.image_to_string(imagem, lang="por")
    else:
        raise ValueError("Formato não suportado. Use PDF ou imagem.")

def extrair_dados(texto: str) -> dict:
    cliente_match = re.search(r"(?i)Cliente:\s*(.+)", texto)
    cliente = cliente_match.group(1).strip() if cliente_match else "Não encontrado"

    vencimento_match = re.search(r"\b(\d{2}/\d{2}/\d{4})\b", texto)
    vencimento = vencimento_match.group(1) if vencimento_match else "Não encontrado"

    valor_match = re.search(
        r"(?i)(?:valor (?:do )?documento)[^\d]*(\d{1,3}(?:\.\d{3})*,\d{2})", texto
    )

    if valor_match:
        valor = valor_match.group(1)
    else:
        valores = re.findall(r"\d{1,3}(?:\.\d{3})*,\d{2}", texto)
        valores_float = [float(v.replace('.', '').replace(',', '.')) for v in valores]
        valor_maior = max(valores_float, default=None)
        valor = f"{valor_maior:,.2f}".replace('.', ',') if valor_maior else "Não encontrado"

    return {
        "Cliente": cliente,
        "Vencimento": vencimento,
        "Valor": f"R$ {valor}" if valor != "Não encontrado" else valor
    }

# === GUI (tkinter) ===

def selecionar_arquivo():
    caminho = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=[("PDF e Imagens", "*.pdf *.png *.jpg *.jpeg")]
    )

    if not caminho:
        return

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

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar o arquivo:\n{e}")

# Interface principal
janela = tk.Tk()
janela.title("🔍 Leitor de Boletos / PDFs")
janela.geometry("780x650")
janela.configure(bg="#f2f2f2")
janela.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", font=("Segoe UI", 11), padding=10, background="#4CAF50", foreground="white")
style.map("TButton", background=[("active", "#45a049")])

# Botão de seleção
btn_arquivo = ttk.Button(janela, text="📂 Selecionar Arquivo", command=selecionar_arquivo)
btn_arquivo.pack(pady=20)

# Área de texto extraído
texto_frame = tk.Frame(janela, bg="#f2f2f2")
texto_frame.pack(pady=10, padx=10)

texto_area = scrolledtext.ScrolledText(
    texto_frame, wrap=tk.WORD, width=90, height=18,
    font=("Courier New", 10), borderwidth=2, relief="groove", bg="white"
)
texto_area.pack()
texto_area.config(state='disabled')

# Campos de dados extraídos
frame_dados = tk.Frame(janela, bg="#f2f2f2")
frame_dados.pack(pady=20)

cliente_var = tk.StringVar()
vencimento_var = tk.StringVar()
valor_var = tk.StringVar()

def criar_linha(label, var, row, emoji):
    tk.Label(frame_dados, text=f"{emoji} {label}:", font=("Segoe UI", 10, "bold"), bg="#f2f2f2").grid(row=row, column=0, sticky="w", padx=5, pady=5)
    ttk.Entry(frame_dados, textvariable=var, width=60).grid(row=row, column=1, padx=5, pady=5)

criar_linha("Cliente", cliente_var, 0, "👤")
criar_linha("Vencimento", vencimento_var, 1, "📅")
criar_linha("Valor", valor_var, 2, "💰")

# Rodapé
rodape = tk.Label(janela, text="Desenvolvido por Mehran • v1.1", font=("Segoe UI", 9), fg="gray", bg="#f2f2f2")
rodape.pack(pady=10)

janela.mainloop()
