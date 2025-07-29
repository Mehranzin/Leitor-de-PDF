import os
import re
from PIL import Image, ImageFilter
import pytesseract
import pdfplumber

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # ajuste se necessário

def extrair_dados(texto):
    cliente = re.search(r"(?i)Cliente:\s*(.+)", texto)
    nome_cliente = cliente.group(1).strip() if cliente else "Não encontrado"

    venc = re.search(r"\d{2}/\d{2}/\d{4}", texto)
    vencimento = venc.group(0) if venc else "Não encontrado"

    valor_match = re.search(r"(?i)(?:(?<=valor documento)|(?<=valor do documento)).*?(\d{1,3}(?:\.\d{3})*,\d{2})", texto)
    if not valor_match:
        valores = re.findall(r"\d{1,3}(?:\.\d{3})*,\d{2}", texto)
        valores_float = [float(v.replace('.', '').replace(',', '.')) for v in valores]
        maior_valor = max(valores_float) if valores_float else None
        valor_final = f"{maior_valor:,.2f}".replace('.', ',') if maior_valor else "Não encontrado"
    else:
        valor_final = valor_match.group(1)

    dados = {
        "Cliente": nome_cliente,
        "Valor": f"R$ {valor_final}" if valor_final else "Não encontrado",
        "Vencimento": vencimento
    }

    print("\n📄 Dados extraídos:")
    for chave, valor in dados.items():
        print(f"- {chave}: {valor}")

def preprocessar_imagem(caminho):
    imagem = Image.open(caminho).convert('L')
    imagem = imagem.filter(ImageFilter.SHARPEN)
    imagem = imagem.point(lambda x: 0 if x < 140 else 255)
    return imagem

def extrair_texto(caminho):
    if caminho.lower().endswith('.pdf'):
        with pdfplumber.open(caminho) as pdf:
            texto = ""
            for pagina in pdf.pages:
                texto += pagina.extract_text() + "\n"
            return texto
    elif caminho.lower().endswith(('.png', '.jpg', '.jpeg')):
        imagem = preprocessar_imagem(caminho)
        return pytesseract.image_to_string(imagem, lang='por')
    else:
        raise ValueError("Formato não suportado. Use PDF ou imagem.")

if __name__ == "__main__":
    print("Arraste o arquivo PDF ou imagem aqui ou digite o caminho completo:")
    caminho = input(">>> ").strip().replace("& ", "").strip('"').strip("'")

    if not os.path.exists(caminho):
        print("Arquivo não encontrado.")
    else:
        try:
            texto = extrair_texto(caminho)
            print("\n📝 Texto cru extraído:")
            print(texto)
            extrair_dados(texto)
        except Exception as e:
            print(f"Erro ao processar o arquivo: {e}")
