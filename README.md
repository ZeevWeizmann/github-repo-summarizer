# GitHub Repository Summarizer API

Author: Zeev Weizmann

Personal ID: 678524131523

This project implements an API service that takes a public GitHub repository URL and returns a structured summary of the project using an LLM (Nebius Token Factory API).

The API extracts key repository information (README, file structure, recent commits) and sends a condensed context to the LLM to generate a
human-readable summary.

This high-level repository metadata provides a strong signal for the LLM to produce an informative overview. Inspecting the full contents of source files was intentionally avoided, as it would significantly increase complexity and token usage without proportionally improving summary quality for this task.

Another reason for prioritizing key repository information is the preference for human-written content, which typically provides clearer intent and higher-level semantics than auto-generated artifacts.

---

## Setup Instructions (from a clean machine)

Assume Python 3.10+ is installed.

### 1. Clone the repository

```bash
git clone https://github.com/ZeevWeizmann/github-repo-summarizer.git
cd github-repo-summarizer
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux

# On Windows:
# venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

macOS/Linux:

```bash
export NEBIUS_API_KEY=your_api_key_here
export OPENAI_BASE_URL=https://api.studio.nebius.ai/v1
export MODEL=meta-llama/Meta-Llama-3.1-8B-Instruct
```

Windows (PowerShell):

```powershell
setx NEBIUS_API_KEY "your_api_key_here"
setx OPENAI_BASE_URL "https://api.studio.nebius.ai/v1"
setx MODEL "meta-llama/Meta-Llama-3.1-8B-Instruct"
```

Do not hardcode API keys.

### 5. Start the server

```bash
uvicorn main:app --reload
```

The server will start at:

http://localhost:8000

### 6. Test the endpoint

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"github_url": "https://github.com/psf/requests"}'
```

The API returns a structured JSON response containing a concise project summary, detected technologies, and repository structure overview.

Expected response:

```
{
  "summary": "Requests is a simple, yet elegant, HTTP library for Python that allows you to send HTTP/1.1 requests extremely easily.",
  "technologies": ["Python", "HTTP", "GitHub"],
  "structure": "The repository contains a Makefile, a README.md, and various directories for documentation, tests, and source code."
}
```

---

## Model Choice

The model used is `meta-llama/Meta-Llama-3.1-8B-Instruct` via Nebius
Token Factory.

The 8B parameter size offers enough representational capacity for accurate high-level summarization while maintaining reasonable cost for an API service.

---

## Repository Processing Strategy

Repositories can be large, so sending everything to the LLM is not
feasible.

### Included

- README (first 3000 characters)
- Filtered file tree (first 200 relevant files)
- Recent commit messages (filtered and truncated)

### Skipped

- Binary files (.png, .jpg, .zip, .pdf, etc.)
- Lock files (poetry.lock, yarn.lock, package-lock.json)
- Build artifacts (dist/, build/)
- Virtual environments (.venv/)
- node_modules/

### Context management

- README truncated to 3000 characters
- File tree limited to first 200 files
- Commits truncated to 1500 characters

This ensures the context window is respected while preserving the most
informative signals.

---

## Error Handling

The API handles the following error scenarios:

- Invalid GitHub URLs (400)
- Repository access errors, including non-existing or private repositories (400)
- Unexpected server errors (500)

All errors are returned as structured JSON responses in the following format:

```
{
"status": "error",
"message": "Description of what went wrong"
}
```

In cases where partial GitHub metadata cannot be retrieved (e.g., commits or file tree),
the service degrades gracefully by returning empty sections instead of failing entirely.

---

## Project Structure

- `main.py` – FastAPI application entry point and `/summarize` endpoint
- `models.py` – Pydantic request schema for validating input
- `github_service.py` – GitHub API interaction and repository filtering logic
- `llm_service.py` – LLM integration via Nebius Token Factory (OpenAI-compatible API)
- `requirements.txt` – Project dependencies
- `.gitignore` – Excludes virtual environments, cache files, and sensitive data

---

## Repository & Links

- **GitHub Repository:**  
  https://github.com/ZeevWeizmann/github-repo-summarizer

- **Project Page (GitHub Pages):**  
  https://zeevweizmann.github.io/github-repo-summarizer/
