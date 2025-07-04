#!/bin/bash

# Script to reset PR comments for testing the Code Review Panel feature
# This will delete all comments from the PR to allow fresh testing

PR_NUMBER=1
OWNER="srao-positron"
REPO="test-code-review-repo"

echo "Resetting comments on PR #$PR_NUMBER..."

# Get all issue comments (general PR comments)
echo "Fetching general PR comments..."
ISSUE_COMMENTS=$(gh api repos/$OWNER/$REPO/issues/$PR_NUMBER/comments --jq '.[].id')

# Delete each issue comment
for comment_id in $ISSUE_COMMENTS; do
    echo "Deleting issue comment $comment_id..."
    gh api -X DELETE repos/$OWNER/$REPO/issues/comments/$comment_id
done

# Get all review comments (line-specific comments)
echo "Fetching review comments..."
REVIEW_COMMENTS=$(gh api repos/$OWNER/$REPO/pulls/$PR_NUMBER/comments --jq '.[].id')

# Delete each review comment
for comment_id in $REVIEW_COMMENTS; do
    echo "Deleting review comment $comment_id..."
    gh api -X DELETE repos/$OWNER/$REPO/pulls/comments/$comment_id
done

echo "All comments have been deleted from PR #$PR_NUMBER"
echo "PR is ready for fresh code review testing!"