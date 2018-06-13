#!/bin/bash
curl -o /tmp/travis-automerge https://raw.githubusercontent.com/cdown/travis-automerge/master/travis-automerge
chmod a+x /tmp/travis-automerge
BRANCHES_TO_MERGE_REGEX='^master' BRANCH_TO_MERGE_INTO=deployment GITHUB_REPO=sjoerdwels/thefuck /tmp/travis-automerge