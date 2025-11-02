# 📚 Gen-AI Repository Workflow

## Overview

This repository (`gen-ai`) contains your personal AI projects that you want to share publicly. It's separate from the course repository (`agents`) to keep things organized.

## Directory Structure

```
/Users/gkeskar/projects/
├── agents/           ← Course repo (ed-donner/agents)
│   └── 2_openai/
│       └── code_learning_assistant/  ← Work here
└── gen-ai/           ← Your public repo (gkeskar/gen-ai)
    └── code-assistant/                ← Push here
```

## Simple Workflow

### Step 1: Work on Your Project in `agents/`

Do all your development in the course repository:

```bash
cd /Users/gkeskar/projects/agents/2_openai/code_learning_assistant
# Make changes, test, etc.
```

### Step 2: Sync to `gen-ai` When Ready to Share

Use the sync script to copy your project:

```bash
cd /Users/gkeskar/projects/gen-ai
./sync-project.sh code_learning_assistant
```

This will:
- Copy files from `agents/2_openai/code_learning_assistant/code-assistant/` 
- To `gen-ai/code-assistant/`
- Excluding temp files and build artifacts

### Step 3: Commit and Push

```bash
cd /Users/gkeskar/projects/gen-ai
git status                    # Review changes
git add .
git commit -m "Your message"
git push origin main
```

That's it! ✅

## Quick Reference

### Check What Changed
```bash
cd /Users/gkeskar/projects/gen-ai
git status
git diff
```

### View Remote URL
```bash
cd /Users/gkeskar/projects/gen-ai
git remote -v
# Should show: origin git@github.com-personal:gkeskar/gen-ai.git
```

### Pull Latest from GitHub
```bash
cd /Users/gkeskar/projects/gen-ai
git pull origin main
```

## Adding New Projects

To add a new project from the course repo:

1. **Create sync command** for your new project in `sync-project.sh`
2. **Run the sync:**
   ```bash
   ./sync-project.sh your_new_project
   ```
3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add new project: your_new_project"
   git push origin main
   ```

## Important Notes

### ✅ This Repository is for:
- Your completed projects
- Code you want to share publicly
- Portfolio work

### ❌ Don't Push:
- `.env` files (already in `.gitignore`)
- API keys or secrets
- Personal notes with sensitive info
- Large binary files

### Git Setup

This repo uses your personal GitHub SSH key configured in `~/.ssh/config`:
```
Host github.com-personal
HostName github.com
User git
IdentityFile ~/.ssh/id_rsa_gkeskar
```

The remote URL uses `github.com-personal` to ensure the correct SSH key is used.

## Troubleshooting

### Problem: Permission denied when pushing

**Solution:** Make sure you're using the correct SSH key
```bash
cd /Users/gkeskar/projects/gen-ai
git remote -v
# Should show: git@github.com-personal:gkeskar/gen-ai.git
```

### Problem: Can't find .env file in code-assistant

**Solution:** The code automatically searches upward for `.env` file. Make sure you have a `.env` in the projects root or in your home directory.

### Problem: Want to undo changes

**Solution:** 
```bash
cd /Users/gkeskar/projects/gen-ai
git checkout .           # Discard all changes
git checkout main        # Switch to main branch
git pull origin main     # Get latest from GitHub
```

---

**🎯 Key Principle:** Work in `agents/`, sync to `gen-ai`, push to GitHub. Keep it simple!

