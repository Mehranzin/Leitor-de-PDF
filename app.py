import os
import re
from PIL import Image, ImageFilter
import pytesseract
import pdfplumber

# Ajuste o caminho do Tesseract se necessário
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extrair_dados(texto: str) -> dict:
    """Extrai cliente, valor e vencimento do texto OCR."""
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
        # Tenta extrair o maior valor numérico se o campo específico não for encontrado
        valores = re.findall(r"\d{1,3}(?:\.\d{3})*,\d{2}", texto)
        valores_float = [float(v.replace('.', '').replace(',', '.')) for v in valores]
        valor_maior = max(valores_float, default=None)
        valor = f"{valor_maior:,.2f}".replace('.', ',') if valor_maior else "Não encontrado"

    return {
        "Cliente": cliente,
        "Vencimento": vencimento,
        "Valor": f"R$ {valor}" if valor != "Não encontrado" else valor
    }

def preprocessar_imagem(caminho: str) -> Image.Image:
    """Aplica pré-processamento básico para melhorar o OCR."""
    imagem = Image.open(caminho).convert("L")  # Converte para tons de cinza
    imagem = imagem.filter(ImageFilter.SHARPEN)  # Aumenta nitidez
    imagem = imagem.point(lambda x: 0 if x < 140 else 255)  # Binarização
    return imagem

def extrair_texto(caminho: str) -> str:
    """Extrai texto de um arquivo PDF ou imagem."""
    if caminho.lower().endswith(".pdf"):
        with pdfplumber.open(caminho) as pdf:
            return "\n".join(pagina.extract_text() or "" for pagina in pdf.pages)
    elif caminho.lower().endswith((".png", ".jpg", ".jpeg")):
        imagem = preprocessar_imagem(caminho)
        return pytesseract.image_to_string(imagem, lang="por")
    else:
        raise ValueError("Formato não suportado. Use PDF ou imagem (JPG/PNG).")

def limpar_caminho(caminho_bruto: str) -> str:
    """Remove caracteres desnecessários do input do usuário."""
    return caminho_bruto.strip().replace("& ", "").strip('"').strip("'")

def mostrar_resultados(dados: dict):
    """Exibe os dados extraídos no terminal."""
    print("\n📄 Dados extraídos:")
    for chave, valor in dados.items():
        print(f"- {chave}: {valor}")

def main():
    print("📂 Arraste o arquivo PDF ou imagem aqui ou digite o caminho completo:")
    caminho_input = input(">>> ")
    caminho = limpar_caminho(caminho_input)

    if not os.path.isfile(caminho):
        print("❌ Arquivo não encontrado.")
        return

    try:
        texto = extrair_texto(caminho)
        print("\n📝 Texto extraído:")
        print(texto)
        dados = extrair_dados(texto)
        mostrar_resultados(dados)
    except Exception as erro:
        print(f"⚠️ Erro ao processar o arquivo: {erro}")

if __name__ == "__main__":
    main()
