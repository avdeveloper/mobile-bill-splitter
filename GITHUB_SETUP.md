# GitHub Setup Guide

Follow these steps to upload this project to GitHub.

## Prerequisites

- Git installed on your system
- A GitHub account
- GitHub CLI (`gh`) installed (optional, makes it easier)

## Steps to Upload to GitHub

### Option 1: Using GitHub CLI (Recommended)

```bash
# 1. Initialize git repository
git init

# 2. Add all files (respects .gitignore)
git add .

# 3. Create initial commit
git commit -m "Initial commit: T-Mobile bill splitter tool"

# 4. Create GitHub repository and push
gh repo create tmobile-bill-splitter --public --source=. --push

# Or for private repo:
# gh repo create tmobile-bill-splitter --private --source=. --push
```

### Option 2: Using GitHub Website

```bash
# 1. Initialize git repository
git init

# 2. Add all files (respects .gitignore)
git add .

# 3. Create initial commit
git commit -m "Initial commit: T-Mobile bill splitter tool"

# 4. Go to GitHub.com and create a new repository named "tmobile-bill-splitter"

# 5. Connect and push
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/tmobile-bill-splitter.git
git push -u origin main
```

## Verify What Will Be Committed

Before committing, verify that personal files are excluded:

```bash
# Check git status
git status

# Files that should appear (tracked):
# - .gitignore
# - LICENSE
# - README.md
# - requirements.txt
# - split_bill.py
# - split_bill.sh
# - phone_names.txt.example

# Files that should NOT appear (ignored):
# - *.pdf (bills)
# - *_split.csv (generated CSVs)
# - phone_names.txt (personal mapping)
# - venv/ (Python environment)
```

## After Uploading

1. Go to your repository on GitHub
2. Add topics/tags: `python`, `cli`, `bill-splitter`, `tmobile`, `family-plan`
3. Add a description: "CLI tool to fairly split T-Mobile family plan bills"
4. Consider enabling GitHub Issues for bug reports and feature requests

## Keeping Your Fork Updated

If you forked this project and want to keep it updated:

```bash
# Add upstream remote
git remote add upstream https://github.com/original-author/tmobile-bill-splitter.git

# Fetch and merge updates
git fetch upstream
git merge upstream/main
```

## Important Reminders

⚠️ **Privacy**: The `.gitignore` file is configured to exclude:
- Your bill PDFs
- Generated CSV files
- Your personal phone_names.txt file
- Python virtual environment

✅ **Double-check** before pushing that no personal data is included:
```bash
git log --stat  # Review what's in your commit
```

🔒 **If you accidentally commit personal data**:
```bash
# Remove file from git but keep local copy
git rm --cached filename.pdf
git commit -m "Remove accidentally committed file"
git push

# For sensitive data already pushed, consider using:
# https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
```
