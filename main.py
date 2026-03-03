"""Main application file for the GitHub repository summarizer API."
"""
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from models import RepoRequest
from github_service import fetch_readme, fetch_tree, fetch_commits
from llm_service import summarize_text


app = FastAPI()



    
@app.post("/summarize")
def summarize(request: RepoRequest):
    try:
        readme = fetch_readme(request.github_url)
        tree = fetch_tree(request.github_url)
        commits = fetch_commits(request.github_url)

        context = f"""
Repository structure:
{tree[:3000]}

Recent commits:
{commits}

README:
{readme[:3000]}
"""

        result = summarize_text(context)
        return result

    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": str(e)
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Internal server error"
            }
        )
