# artbot

Standalone repository scaffold for the art automation bootstrap logic.

## What this contains

- `run_colab.py`: a Python script extracted from the original Colab notebook cell.
  It discovers the active notebook session, resolves the corresponding raw GitHub
  URL, and downloads the target script.

## Quick start

```bash
python -m pip install -r requirements.txt
python run_colab.py
```

> Note: this flow expects a running Jupyter/Colab server session.

## Create a dedicated GitHub repo named `artbot`

From this folder, you can initialize and push to a new repository:

```bash
git init
git add .
git commit -m "Initial artbot scaffold"
git branch -M main
git remote add origin git@github.com:<your-user>/artbot.git
git push -u origin main
```
