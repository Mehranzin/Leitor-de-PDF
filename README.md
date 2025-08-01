# 📄 PDF and Invoice Reader

---

## 🇬🇧 ENGLISH

This is a simple project designed to extract key information from PDF and image files of invoices and documents, such as client name, due date, amount, and CPF/CNPJ. It's built with Python, leveraging Tkinter for the graphical interface and Tesseract OCR for text recognition.

### ✨ Features

- **Multi-Format Support**: Reads PDFs, PNGs, JPGs, and JPEGs.
- **Smart Extraction**: Automatically identifies and organizes data including:
  - Client
  - Due Date
  - Amount
  - CPF/CNPJ
- **Intuitive Interface**: Easily drag-and-drop your files or select them manually.
- **Dark Mode**: Switch between light and dark themes for enhanced visual comfort.
- **Image Pre-processing**: Improves image quality for more accurate text extraction.

### 🚀 How to Use

1.  **Install Python Dependencies**:
    You can install the necessary libraries using `pip`:

    ```bash
    pip install Pillow pytesseract pdfplumber openpyxl tkdnd
    ```

    **Note**: `tkdnd` is required for the drag-and-drop functionality. You might need to install the `tkinterdnd2` package manually via pip or ensure your Tkinter environment supports DnD.

2.  **Run the Program**:
    After installing everything, simply run the Python script:

    ```bash
    python your_main_file.py
    ```

    The application window will open, allowing you to select or drag your files to extract information.

### 🛠️ Technologies Used

- **Python**: The core language of the project.
- **Tkinter**: For the Graphical User Interface (GUI).
- **TkinterDnD2**: Provides drag-and-drop capabilities.
- **Pillow (PIL)**: Image processing library.
- **Pytesseract**: Python wrapper for Tesseract OCR (text recognition).
- **Pdfplumber**: Extracts text and images from PDFs.
- **OpenPyXL**: For future Excel file manipulation (currently not directly used in extraction but present in your original code's dependencies).

---

## 🇧🇷 PORTUGUÊS

Este é um projeto simples para extrair informações importantes de PDFs e imagens de boletos e documentos, como cliente, data de vencimento, valor e CPF/CNPJ. Ele foi desenvolvido com Python, utilizando Tkinter para a interface gráfica e Tesseract OCR para o reconhecimento de texto.

### ✨ Funcionalidades

- **Leitura de Múltiplos Formatos**: Suporta PDFs, PNGs, JPGs e JPEGs.
- **Extração Inteligente**: Identifica e organiza automaticamente dados como:
  - Cliente
  - Vencimento
  - Valor
  - CPF/CNPJ
- **Interface Intuitiva**: Arraste e solte seus arquivos ou selecione-os manualmente.
- **Modo Escuro**: Alterne entre temas claro e escuro para maior conforto visual.
- **Pré-processamento de Imagens**: Melhora a qualidade das imagens para uma extração de texto mais precisa.

### 🚀 Como Usar

1.  **Instale as Dependências Python**:
    Você pode instalar as bibliotecas necessárias usando `pip`:

    ```bash
    pip install Pillow pytesseract pdfplumber openpyxl tkdnd
    ```

    **Nota**: `tkdnd` é necessária para a funcionalidade de arrastar e soltar. Pode ser que você precise instalar o pacote `tkinterdnd2` manualmente via pip ou garantir que seu ambiente Tkinter suporte DnD.

2.  **Execute o Programa**:
    Após instalar tudo, basta rodar o script Python:

    ```bash
    python seu_arquivo_principal.py
    ```

    A janela do aplicativo se abrirá, permitindo que você selecione ou arraste seus arquivos para extrair as informações.

### 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **Tkinter**: Para a interface gráfica (GUI).
- **TkinterDnD2**: Funcionalidade de arrastar e soltar.
- **Pillow (PIL)**: Processamento de imagens.
- **Pytesseract**: Interface Python para o Tesseract OCR (reconhecimento de texto).
- **Pdfplumber**: Extração de texto e imagens de PDFs.
- **OpenPyXL**: Para manipulação futura de arquivos Excel (atualmente não utilizada diretamente na extração, mas presente nas dependências do seu código original).

---

Mehran Louksa Mesrob
"flow.page/mehranlouksa"
'