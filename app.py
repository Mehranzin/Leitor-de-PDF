import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from PIL import Image, ImageFilter
import pytesseract
import pdfplumber

# Caminho do Tesseract (ajuste conforme necessário)
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

        texto_area.delete(1.0, tk.END)
        texto_area.insert(tk.END, texto)

        cliente_var.set(dados["Cliente"])
        vencimento_var.set(dados["Vencimento"])
        valor_var.set(dados["Valor"])

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar o arquivo:\n{e}")

# Interface principal
janela = tk.Tk()
janela.title("Leitor de Boletos / PDFs")
janela.geometry("700x600")
janela.resizable(False, False)

# Botão de seleção
btn_arquivo = tk.Button(janela, text="📂 Selecionar Arquivo", command=selecionar_arquivo, font=("Arial", 12))
btn_arquivo.pack(pady=10)

# Área de texto extraído
texto_area = scrolledtext.ScrolledText(janela, wrap=tk.WORD, width=80, height=15, font=("Courier New", 10))
texto_area.pack(pady=10)

# Campos de dados extraídos
frame_dados = tk.Frame(janela)
frame_dados.pack(pady=10)

cliente_var = tk.StringVar()
vencimento_var = tk.StringVar()
valor_var = tk.StringVar()

tk.Label(frame_dados, text="👤 Cliente:", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
tk.Entry(frame_dados, textvariable=cliente_var, width=60).grid(row=0, column=1)

tk.Label(frame_dados, text="📅 Vencimento:", font=("Arial", 10)).grid(row=1, column=0, sticky="w")
tk.Entry(frame_dados, textvariable=vencimento_var, width=60).grid(row=1, column=1)

tk.Label(frame_dados, text="💰 Valor:", font=("Arial", 10)).grid(row=2, column=0, sticky="w")
tk.Entry(frame_dados, textvariable=valor_var, width=60).grid(row=2, column=1)

# Rodapé
tk.Label(janela, text="Desenvolvido por Mehran • v1.0", fg="gray").pack(pady=10)

janela.mainloop()
