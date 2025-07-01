from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from github_utils import clone_and_get_commits
from github_search import find_similar_repo
from diff_utils import get_diffs
from ai_similarity import compute_similarity_score
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_repo(repo_url: str = Form(...)):
    user_repo_path, commit_dates = clone_and_get_commits(repo_url)
    match_url, match_path = find_similar_repo(user_repo_path)

    result = {
        "commit_start": commit_dates[0],
        "commit_end": commit_dates[-1],
        "match_repo": match_url
    }

    if match_url:
        diffs = get_diffs(user_repo_path, match_path)
        similarity, score = compute_similarity_score(user_repo_path, match_path)
        result.update({
            "similarity_score": similarity,
            "plagiarism_score": score,
            "diffs": diffs
        })
    return result