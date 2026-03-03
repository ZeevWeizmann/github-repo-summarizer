
import requests

def parse_github_url(github_url: str):
    parts = github_url.rstrip("/").split("/")

    if "github.com" not in github_url or len(parts) < 5:
        raise ValueError("Invalid GitHub URL")

    return parts[-2], parts[-1]

def fetch_readme(github_url: str):
    owner, repo = parse_github_url(github_url)

    api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    r = requests.get(api_url)

    if r.status_code == 404:
        return ""
    elif r.status_code != 200:
        raise ValueError("Cannot fetch README")

    download_url = r.json()["download_url"]
    readme_text = requests.get(download_url).text

    return readme_text

def fetch_tree(github_url: str):
    owner, repo = parse_github_url(github_url)

    repo_info = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}"
    )

    if repo_info.status_code != 200:
        raise ValueError("Cannot fetch repository info")

    branch = repo_info.json()["default_branch"]

    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    r = requests.get(tree_url)

    if r.status_code != 200:
        return ""

    files = []

    for item in r.json().get("tree", []):
        path = item["path"]

        if any(skip in path for skip in ["node_modules", "dist", "build", ".venv"]):
            continue
        if path.endswith((".png", ".jpg", ".jpeg", ".gif", ".zip", ".pdf")):
            continue
        if path.endswith(("package-lock.json", "poetry.lock", "yarn.lock")):
            continue

        files.append(path)

    return "\n".join(files[:200])

def fetch_commits(github_url: str):
    owner, repo = parse_github_url(github_url)

    commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=20"
    r = requests.get(commits_url)

    if r.status_code != 200:
        return ""

    messages = []

    for commit in r.json():
        message = commit["commit"]["message"].strip()

        if len(message) < 10:
            continue

        first_line = message.split("\n")[0]
        messages.append(first_line)

    commits_text = "\n".join(messages)

    return commits_text[:1500]
