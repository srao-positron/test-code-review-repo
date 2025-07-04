#!/bin/bash

# Script to create a new PR for testing the Code Review Panel feature
# This creates a new branch with a small change and opens a PR

OWNER="srao-positron"
REPO="test-code-review-repo"
TIMESTAMP=$(date +%Y%m%d%H%M%S)
BRANCH_NAME="feature/test-$TIMESTAMP"

echo "Creating new test PR..."

# Ensure we're on main branch and up to date
git checkout main
git pull origin main

# Create new branch
git checkout -b $BRANCH_NAME

# Make a small change (add a comment to README)
echo "" >> README.md
echo "<!-- Test change $TIMESTAMP -->" >> README.md

# Commit the change
git add README.md
git commit -m "Test change for code review demo $TIMESTAMP"

# Push the branch
git push -u origin $BRANCH_NAME

# Create PR
PR_URL=$(gh pr create \
    --title "Test PR for Code Review Demo - $TIMESTAMP" \
    --body "This is a test PR created for demonstrating the Code Review Panel feature.

## Test Change
Added a timestamp comment to README.md

## Purpose
This PR is intended to be reviewed by the AI code review panel to demonstrate the feature." \
    --base main)

echo "Created new PR: $PR_URL"

# Extract PR number from URL
PR_NUMBER=$(echo $PR_URL | grep -oE '[0-9]+$')

# Update reset script with new PR number
sed -i '' "s/PR_NUMBER=.*/PR_NUMBER=$PR_NUMBER/" reset-pr-comments.sh

echo "Updated reset-pr-comments.sh with PR number: $PR_NUMBER"