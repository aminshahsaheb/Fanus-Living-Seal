#!/bin/bash

echo "🧠 FANUS SAFE SYNC START"

# 1. check repo
if [ ! -d ".git" ]; then
  echo "❌ Not a git repository"
  exit 1
fi

# 2. abort any rebase automatically
if [ -d ".git/rebase-merge" ] || [ -d ".git/rebase-apply" ]; then
  echo "⚠️ Rebase detected → aborting safely"
  git rebase --abort
fi

# 3. check status
STATUS=$(git status --porcelain)

if [ -n "$STATUS" ]; then
  echo "📝 Changes detected → staging..."

  git add .

  git commit -m "auto-sync: safe checkpoint"

else
  echo "✅ No changes to commit"
fi

# 4. pull safely
echo "⬇️ Pulling latest changes..."
git pull --rebase origin main

# 5. push
echo "⬆️ Pushing to origin..."
git push origin main

echo "✅ FANUS SYNC COMPLETE"
