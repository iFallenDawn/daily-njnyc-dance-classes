# Daily NJ/NYC Dance Classes Backend

## Prereqs
linux machine or wsl lmao
```bash
cd backend/
uv sync
source .venv/bin/activate
```
may need to change python interpreter in vscode to `.venv/bin/python3.13

## how to migrate pyproject.toml to requirements.txt
```bash
uv pip compile pyproject.toml -o requirements.txt
```