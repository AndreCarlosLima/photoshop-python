# Photoshop em Python

Aplicação web simples para carregar imagens e aplicar edições básicas usando
Flask e Pillow.

## Funcionalidades

- Upload de imagens
- Rotação para a esquerda ou para a direita
- Conversão para preto e branco
- Aplicação de efeito sépia
- Download da imagem editada

## Como executar localmente

1. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

   No Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Inicie a aplicação:

   ```bash
   python app.py
   ```

4. Abra <http://127.0.0.1:5000> no navegador.

As imagens enviadas durante o uso ficam em `static/uploads/`. Essa pasta é
ignorada pelo Git para evitar publicar imagens pessoais ou arquivos gerados
localmente.
