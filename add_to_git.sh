#!/bin/bash

# Display git status
git status

# Get list of modified files
files=$(git status -s | awk '{print $2}')

# Check if there are modified files
if [ -z "$files" ]; then
  echo "No modified files to add."
  exit 0
fi

# Loop through each modified file and prompt to add
for file in $files; do
  read -p "Do you want to add '$file'? (y/n): " choice
  if [ "$choice" = "y" ]; then
    # Add the file
    git add "$file"
    echo "'$file' added to staging area."
  else
    echo "'$file' not added."
  fi
done

exit 0

