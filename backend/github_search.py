import requests, os, shutil
from git import Repo
from urllib.parse import quote
from dotenv import load_dotenv
def search_code_snippets(path):
    code_sample = ""
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(".py"):
                with open(os.path.join(root, f)) as file:
                    code_sample += ''.join(file.readlines()[:20])  # take first 20 lines
        break
    return code_sample[:300]

def find_similar_repo(user_repo_path):
    load_dotenv()

    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}", "Accept": "application/vnd.github+json"}
    query = quote(search_code_snippets(user_repo_path))
    url = f"https://api.github.com/search/code?q={query}+in:file+language:python"
    res = requests.get(url, headers=headers).json()
    if "items" in res and res["items"]:
        item = res["items"][0]
        repo_url = item["repository"]["html_url"]
        path = f"/tmp/original_repo"
        if os.path.exists(path):
            shutil.rmtree(path)
        Repo.clone_from(repo_url, path)
        return repo_url, path
    return None, None