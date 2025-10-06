import os
import openai
import requests
import base64

# Claves y contexto
openai.api_key = os.getenv("OPENAI_API_KEY")
repo = os.getenv("GITHUB_REPOSITORY")
pr_number = os.getenv("GITHUB_PR_NUMBER")
gh_token = os.getenv("GITHUB_TOKEN")

headers = {"Authorization": f"token {gh_token}"}

# Obtener cambios del PR
files_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
files = requests.get(files_url, headers=headers).json()

comments = []

for file in files:
    filename = file["filename"]
    patch = file.get("patch", "")
    if not patch:
        continue

    prompt = f"Revisa los siguientes cambios en {filename} y sugiere mejoras o posibles problemas:\n\n{patch}"

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    comments.append(f"**Archivo:** {filename}\n\n{response['choices'][0]['message']['content']}")

# Publicar comentario en el PR
body = "\n\n---\n\n".join(comments)
comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
requests.post(comment_url, headers=headers, json={"body": body})
