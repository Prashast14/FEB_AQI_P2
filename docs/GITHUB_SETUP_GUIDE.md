# GitHub Setup Guide

This guide will walk you through connecting your local Git repository to GitHub.

## Prerequisites
- ✅ Git installed and configured (already done!)
- ✅ Local repository initialized (already done!)
- 🔲 GitHub account (create one at [github.com](https://github.com) if needed)

---

## Step 1: Create a New Repository on GitHub

### Option A: Using GitHub Website (Recommended for beginners)

1. **Go to GitHub**: Open [github.com](https://github.com) and sign in
2. **Create New Repository**:
   - Click the **"+"** icon in the top-right corner
   - Select **"New repository"**
3. **Configure Repository**:
   - **Repository name**: `FEB_AQI_P2` (or any name you prefer)
   - **Description**: "Air Quality Index Analysis Project - Power BI Dashboard"
   - **Visibility**: Choose **Public** or **Private**
   - ⚠️ **IMPORTANT**: 
     - **DO NOT** check "Add a README file"
     - **DO NOT** add .gitignore
     - **DO NOT** choose a license
     - (We already have these files locally!)
4. **Click**: "Create repository"

### Option B: Using GitHub CLI (Advanced)

If you have GitHub CLI installed (`gh`):
```bash
gh repo create FEB_AQI_P2 --public --source=. --remote=origin --push
```

---

## Step 2: Connect Your Local Repository to GitHub

After creating the repository, GitHub will show you setup instructions. Copy the repository URL (it will look like one of these):

- **HTTPS**: `https://github.com/YOUR-USERNAME/FEB_AQI_P2.git`
- **SSH**: `git@github.com:YOUR-USERNAME/FEB_AQI_P2.git`

### Using HTTPS (Easier, recommended)

Run these commands in your project folder:

```bash
# Add GitHub as remote origin
git remote add origin https://github.com/YOUR-USERNAME/FEB_AQI_P2.git

# Rename branch to main (GitHub's default)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

### Using SSH (More secure, requires SSH key setup)

```bash
# Add GitHub as remote origin
git remote add origin git@github.com:YOUR-USERNAME/FEB_AQI_P2.git

# Rename branch to main
git branch -M main

# Push your code to GitHub
git push -u origin main
```

> **Note**: Replace `YOUR-USERNAME` with your actual GitHub username!

---

## Step 3: Authentication

### First Time Pushing (HTTPS)

When you push for the first time using HTTPS, Git will ask for credentials:

- **Username**: Your GitHub username
- **Password**: Use a **Personal Access Token** (NOT your GitHub password)

#### Creating a Personal Access Token (PAT):

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "FEB_AQI_P2 Local Access"
4. Select scopes: Check **"repo"** (full control of private repositories)
5. Click "Generate token"
6. **COPY THE TOKEN** immediately (you won't see it again!)
7. Use this token as your password when Git prompts you

### First Time Pushing (SSH)

You need to set up SSH keys first. See [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

## Step 4: Verify Connection

Check if everything is connected:

```bash
# View remote connections
git remote -v

# Should show:
# origin  https://github.com/YOUR-USERNAME/FEB_AQI_P2.git (fetch)
# origin  https://github.com/YOUR-USERNAME/FEB_AQI_P2.git (push)
```

Visit your GitHub repository page to see your code!

---

## Common Git Commands for Daily Use

### Making Changes and Pushing to GitHub

```bash
# 1. Check what files have changed
git status

# 2. Add files to staging area
git add .                    # Add all changed files
git add <filename>           # Add specific file

# 3. Commit changes with a message
git commit -m "Description of what you changed"

# 4. Push to GitHub
git push

# Or do steps 2-4 in one go for all files:
git add . && git commit -m "Your message" && git push
```

### Viewing History

```bash
# View commit history
git log

# View compact history
git log --oneline

# View last 5 commits
git log -n 5
```

### Pulling Latest Changes

```bash
# If you work from multiple computers or collaborate with others
git pull
```

### Checking Differences

```bash
# See what changed in files
git diff

# See what's staged for commit
git diff --staged
```

---

## Example Workflow

Here's a typical day of work:

```bash
# Morning: Pull latest changes (if any)
git pull

# Make your changes to files...
# (edit code, add data, create dashboards, etc.)

# Afternoon: Save your progress
git add .
git commit -m "Added new AQI analysis for Delhi region"
git push

# Evening: Save final work
git add .
git commit -m "Completed Power BI dashboard for executive summary"
git push
```

---

## Best Practices

### Commit Messages

✅ **Good commit messages:**
- `"Added population data processing script"`
- `"Fixed AQI calculation bug in database query"`
- `"Updated Power BI dashboard with new KPIs"`
- `"Documented API endpoints in README"`

❌ **Bad commit messages:**
- `"Update"`
- `"Fixed stuff"`
- `"Changes"`
- `"asdf"`

### Commit Frequency

- **Commit often**: After completing a logical unit of work
- **Don't wait**: Don't wait until end of day with 50 file changes
- **Atomic commits**: Each commit should represent one logical change

### What to Commit

✅ **DO commit:**
- Source code
- Documentation
- Configuration files (without secrets)
- Small reference data files
- SQL scripts

❌ **DON'T commit:**
- Large data files (>100MB) - use Git LFS or exclude
- Passwords or API keys
- Temporary files
- Database backups
- Your `.env` file with secrets

---

## Troubleshooting

### Problem: "remote origin already exists"

**Solution:**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR-USERNAME/FEB_AQI_P2.git
```

### Problem: "Updates were rejected because the remote contains work"

**Solution:**
```bash
git pull origin main --rebase
git push origin main
```

### Problem: "Failed to push some refs"

**Solution:**
```bash
# Pull first, then push
git pull --rebase
git push
```

### Problem: Authentication failed (HTTPS)

**Solutions:**
1. Make sure you're using a Personal Access Token, not your password
2. Update your credentials:
   ```bash
   git credential-manager erase https://github.com
   ```
3. Try pushing again - it will prompt for credentials

---

## Additional Resources

- [GitHub Documentation](https://docs.github.com)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [GitHub Desktop](https://desktop.github.com/) - GUI alternative to command line

---

## Quick Reference Card

```bash
# Setup (one time)
git remote add origin <URL>
git branch -M main
git push -u origin main

# Daily workflow
git status              # Check status
git add .               # Stage all changes
git commit -m "msg"     # Commit
git push                # Push to GitHub

# View info
git log                 # History
git remote -v           # Show remotes
git status              # Current status

# Get updates
git pull                # Pull from GitHub
```

---

**Your Git Configuration:**
- Name: Prashast Maurya
- Email: prashastmauryalko@gmail.com
- Local Repo: D:\FEB_AQI_P2

**Ready to connect to GitHub!** 🚀
