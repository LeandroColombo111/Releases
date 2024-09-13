import git
import re
from datetime import datetime

repo = git.Repo(".")

categories = {
    "breaking-changes": "Breaking changes",
    "feat": "New features",
    "fix": "Bugfixes",
    "updates": "*"
}

commit_pattern = re.compile(r"\[DS-(\d+)\] - (breaking-changes|feat|fix|updates): (.+)")

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

def update_changelog(new_changelog):
    try:
        with open("CHANGELOG.md", "r") as file:
            current_changelog = file.read()
    except FileNotFoundError:
        current_changelog = ""

    updated_changelog = new_changelog + "\n" + current_changelog
    return updated_changelog


def save_changelog(changelog):
    with open("CHANGELOG.md", "w") as file:
        file.write(changelog)

if __name__ == "__main__":
    merged_prs = get_merged_prs()
    categorized_commits = categorize_commits(merged_prs)
    new_changelog = generate_changelog(categorized_commits)
    updated_changelog = update_changelog(new_changelog)
    save_changelog(updated_changelog)
    print("Changelog actualizado y guardado en CHANGELOG.md")
