import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from github_utils import clone_and_get_commits
from github_search import find_similar_repo
from diff_utils import get_diffs
from ai_similarity import compute_similarity_score

# Load .env environment variables
load_dotenv()
print("OPENAI KEY:", os.getenv("OPENAI_API_KEY"))

# Define app
app = FastAPI()

# CORS config for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class AnalyzeRequest(BaseModel):
    repo_url: str

@app.post("/analyze")
async def analyze_repo(req: AnalyzeRequest):
    repo_url = req.repo_url

    # Step 1: Clone repo and get commit history
    user_repo_path, commit_dates = clone_and_get_commits(repo_url)

    # Step 2: Find most similar repo from GitHub
    match_url, match_path = find_similar_repo(user_repo_path)

    # Base result
    result = {
        "commit_start": commit_dates[0],
        "commit_end": commit_dates[-1],
        "match_repo": match_url
    }

    # Step 3: If match found, compute diff and scores
    if match_url:
        diffs = get_diffs(user_repo_path, match_path)
        similarity, score = compute_similarity_score(user_repo_path, match_path)

        result.update({
            "similarity_score": similarity,
            "plagiarism_score": score,
            "diffs": diffs
        })

    return result
