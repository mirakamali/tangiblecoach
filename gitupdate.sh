#!/bin/bash
set -e

local_branch=$(git rev-parse --symbolic-full-name --abbrev-ref HEAD)
remote_branch=$(git rev-parse --abbrev-ref --symbolic-full-name @{u})
remote=$(git config branch.$local_branch.remote)

echo "Fetching from $remote..."
git fetch $remote

if git merge-base --is-ancestor $remote_branch HEAD; then
    echo 'Already up-to-date'

    exit 0
fi


if git merge-base --is-ancestor HEAD $remote_branch; then
    echo 'Fast-forward possible. Merging...'

    if git merge --ff-only --stat $remote_branch; then
            echo 'pull here'
            sh /home/pi/packagesupdate.sh
            sleep 3
            /usr/bin/sudo reboot

    else
            echo 'treating merge conflicts'

            git fetch --all
            git reset --hard origin/master
            sh /home/pi/packagesupdate.sh
            sleep 4
            /usr/bin/sudo reboot

    fi


else
    echo 'Fast-forward not possible. Rebasing...'
    git rebase --preserve-merges --stat $remote_branch
fi