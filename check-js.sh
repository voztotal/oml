#!/bin/bash

# Basado en https://gist.github.com/linhmtran168/2286aeafe747e78f53bf

TARGET_BRANCH_SHA=$(git rev-parse origin/"${CI_MERGE_REQUEST_TARGET_BRANCH_NAME:-develop}")

STAGED_FILES=$(git diff "${TARGET_BRANCH_SHA}"...HEAD --name-only --diff-filter=ACM | grep ".*\.js$")


if [[ "$STAGED_FILES" = "" ]]; then
  exit 0
fi

PASS=true

if ! command -v eslint 1>/dev/null; then
  echo "Please install ESlint"
  exit 1
fi

echo "Validating Javascript code:"

for FILE in $STAGED_FILES; do
  if eslint "$FILE"; then
    echo "ESLint Passed: $FILE"
  else
    echo "ESLint Failed: $FILE"
    PASS=false
  fi
done

echo "Javascript validation completed!"

if ! $PASS; then
  echo "COMMIT FAILED:\033[0m Your commit contains files that should pass ESLint but do not. Please fix the ESLint errors and try again."
  exit 1
else
  echo "COMMIT SUCCEEDED"
fi

exit $?
