import requests
import os

# 🔹 Configuration
GITHUB_USERNAME = "ton-username"
TOKEN = os.getenv("GITHUB_TOKEN")  # Clé API GitHub
README_PATH = "README.md"

# 🔹 Récupérer les langages des dépôts
def get_languages():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("❌ Erreur lors de la récupération des dépôts")
        return {}

    repos = response.json()
    languages = {}

    for repo in repos:
        lang_url = repo["languages_url"]
        lang_response = requests.get(lang_url, headers=headers)
        if lang_response.status_code == 200:
            for lang, bytes_count in lang_response.json().items():
                languages[lang] = languages.get(lang, 0) + bytes_count

    return languages

# 🔹 Générer le tableau Markdown
def generate_markdown(languages):
    total = sum(languages.values())
    markdown = "## 📊 Langages utilisés\n\n"
    markdown += "| Langage | Pourcentage |\n"
    markdown += "|---------|------------|\n"
    
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total) * 100
        markdown += f"| {lang} | {percentage:.2f}% |\n"

    return markdown

# 🔹 Mettre à jour le README.md
def update_readme():
    languages = get_languages()
    if not languages:
        return
    
    with open(README_PATH, "r", encoding="utf-8") as file:
        content = file.read()

    new_section = generate_markdown(languages)

    # Remplace l'ancienne section si elle existe
    if "## 📊 Langages utilisés" in content:
        content = content.split("## 📊 Langages utilisés")[0] + new_section
    else:
        content += "\n\n" + new_section

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(content)

    print("✅ README.md mis à jour !")

if __name__ == "__main__":
    update_readme()
