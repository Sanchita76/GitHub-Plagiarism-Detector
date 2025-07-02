from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import subprocess
import tempfile
import os
import git
from datetime import datetime

# Load keys
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
print("OPENAI KEY:", OPENAI_KEY[:10], "…")

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoRequest(BaseModel):
    repo_url: str

@app.post("/analyze")
async def analyze_repo(req: RepoRequest):
    repo_url = req.repo_url
    print("Analyzing repo:", repo_url)

    temp_dir = tempfile.mkdtemp()

    try:
        # Clone the GitHub repo
        git.Repo.clone_from(repo_url, temp_dir)

        # Get commit timestamps
        repo = git.Repo(temp_dir)
        commits = list(repo.iter_commits())

        dates = [datetime.fromtimestamp(c.committed_date) for c in commits]
        start_date = min(dates).strftime("%Y-%m-%d")
        end_date = max(dates).strftime("%Y-%m-%d")

        # Dummy values for similarity
        matched_repo = "https://github.com/someuser/original-repo"
        similarity_score = 0.87
        plagiarism_score = round(similarity_score * 100)

        # Dummy diff (can be replaced with real comparison later)
        diffs = [{
            "file": "main.py",
            "diff": "--- original\n+++ cloned\n@@ def hello():\n- print('Hi')\n+ print('Hello')"
        }]

        return {
            "commit_start": start_date,
            "commit_end": end_date,
            "match_repo": matched_repo,
            "similarity_score": similarity_score,
            "plagiarism_score": plagiarism_score,
            "diffs": diffs
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": "Failed to analyze repo"}

    finally:
        # Forcefully delete repo folder using PowerShell
        subprocess.call(['powershell', '-Command', f'Remove-Item -Path "{temp_dir}" -Recurse -Force'])
