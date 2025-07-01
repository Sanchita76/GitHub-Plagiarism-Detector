from git import Repo
import os, shutil
from datetime import datetime

def clone_and_get_commits(repo_url):
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    path = f"/tmp/{repo_name}"
    if os.path.exists(path):
        shutil.rmtree(path)
    repo = Repo.clone_from(repo_url, path)
    commits = list(repo.iter_commits())
    commit_times = sorted([datetime.fromtimestamp(c.committed_date).strftime("%Y-%m-%d %H:%M") for c in commits])
    return path, commit_times