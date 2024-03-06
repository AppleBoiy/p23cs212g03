#!/usr/bin/env bash

git status

read -p "Do you want to commit? (y/n) " -n 1 -r

if [[ $REPLY =~ ^[Yy]$ ]]
then
  echo ""
  git add .
  read -p "Enter commit message: " message
  git commit -m "$message"
  git push
fi

