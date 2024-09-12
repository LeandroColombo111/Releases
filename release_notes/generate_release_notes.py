import git
import re
from datetime import datetime

# Ruta al repositorio local (GitHub Actions manejará esto automáticamente)
repo = git.Repo(".")

# Definir las categorías que nos interesan
categories = { 
    "breaking-changes": "Breaking changes", 
    "feat": "New features", 
    "fix": "bugfixes", 
    "updates": "*" 

}

# Patrón para identificar el formato de commit [DS-###] - tipo: comentario
commit_pattern = re.compile(r"\[DS-(\d+)\] - (feat|fix|chore): (.+)")

# Obtener los PRs/commits mergeados recientes
def get_merged_prs():
    """
    Devuelve una lista de commits que representan PRs mergeados, en formato [DS-###] - tipo: comentario.
    """
    merged_prs = []
    for commit in repo.iter_commits('main', max_count=100):  # Ajustar max_count según necesidad
        message = commit.message
        if "Merge pull request" in message or commit_pattern.match(message):
            merged_prs.append(commit)
    return merged_prs

# Clasificar los commits según el tipo y el formato definido
def categorize_commits(commits):
    categorized_commits = {cat: [] for cat in categories.keys()}

    for commit in commits:
        message = commit.message
        match = commit_pattern.match(message)
        if match:
            ticket_number, commit_type, comment = match.groups()
            formatted_message = f"[DS-{ticket_number}] - {commit_type}: {comment}"
            if commit_type in categories:
                categorized_commits[commit_type].append(formatted_message)

    return categorized_commits

# Generar el changelog en un formato Markdown
def generate_changelog(categorized_commits):
    today = datetime.today().strftime('%Y-%m-%d')
    changelog = f"# Release Notes - {today}\n\n"

    for cat, title in categories.items():
        changelog += f"## {title}\n"
        commits = categorized_commits.get(cat, [])
        if commits:
            for commit in commits:
                changelog += f"- {commit}\n"
        else:
            changelog += f"_No {title.lower()} en esta release._\n"
        changelog += "\n"

    return changelog

# Guardar el changelog en un archivo
def save_changelog(changelog):
    with open("CHANGELOG.md", "w") as file:
        file.write(changelog)

if __name__ == "__main__":
    merged_prs = get_merged_prs()
    categorized_commits = categorize_commits(merged_prs)
    changelog = generate_changelog(categorized_commits)
    save_changelog(changelog)
    print("Changelog generado y guardado en CHANGELOG.md")
