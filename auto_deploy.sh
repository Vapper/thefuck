#!/bin/bash

if [[ $TRAVIS_BRANCH == 'development' ]]
    curl -o /tmp/travis-automerge https://raw.githubusercontent.com/cdown/travis-automerge/master/travis-automerge
    chmod a+x /tmp/travis-automerge
    BRANCHES_TO_MERGE_REGEX='development' BRANCH_TO_MERGE_INTO='master' GITHUB_REPO=sjoerdwels/thefuck /tmp/travis-automerge
fi