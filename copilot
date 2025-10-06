name: ChatGPT Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Instalar dependencias
        run: pip install openai requests

      - name: Ejecutar revisión de ChatGPT
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
          GITHUB_PR_NUMBER: ${{ github.event.pull_request.number }}
        run: python .github/scripts/chatgpt_review.py
