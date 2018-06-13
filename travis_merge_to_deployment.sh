if [ "$TRAVIS_BRANCH" != "master" ]; then
    exit 0;
fi
export GIT_COMMITTER_EMAIL="<your-email>"
export GIT_COMMITTER_NAME="<your-name>"

git config --add remote.origin.fetch +refs/heads/*:refs/remotes/origin/* || exit
git fetch --all || exit
git checkout deployment || exit
git merge --no-ff "$TRAVIS_COMMIT" || exit
git push @github.com/">https://${GITHUB_TOKEN}@github.com/<your-github-user>/<your-repository-name>.git