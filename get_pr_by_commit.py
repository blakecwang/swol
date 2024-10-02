#!/usr/bin/env python

import json
import os
import requests
import sys


token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
sha = sys.argv[1]

assert token, "You must set GITHUB_PERSONAL_ACCESS_TOKEN environment variable"
assert sha, "You must provide a commit sha as an argument"

query = """
query ($repoOwner: String!, $repoName: String!, $sha: String!) {
  repository(name: $repoName, owner: $repoOwner) {
    commit: object(expression: $sha) {
      ... on Commit {
        associatedPullRequests(first: 10) {
          edges {
            node {
              title
              number
              state
              mergedAt
              closedAt
              url
            }
          }
        }
      }
    }
  }
}
"""

variables = {
    "repoOwner": "capitalrx",
    "repoName": "code.capitalrx.com",
    "sha": sha,
}

resp = requests.post(
    'https://api.github.com/graphql',
    json={"query": query, "variables": variables},
    headers={"Authorization": f"Bearer {token}"}
)

body = resp.json()

print(json.dumps(body["data"]["repository"]["commit"]["associatedPullRequests"]["edges"], indent=4))
