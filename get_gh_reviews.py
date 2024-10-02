#!/usr/bin/env python

from collections import Counter
import os
import requests

import arrow


token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")

LOGIN_WHITELIST = [
    "bradfordlemley",
    "saml-caprx",
    "blakecwang",
    "JChoCapRx",
    "rak-crx",
    "nmurphy101",
    "jeremy-cap-rx",
    "dch-cap-rx",
]
START_DATE = arrow.now().shift(weeks=-2)
PLACES = 10

query = """
query($repoOwner: String!, $repoName: String!, $after: String) {
  repository(owner: $repoOwner, name: $repoName) {
    pullRequests(first: 100, after: $after, states: [OPEN, MERGED, CLOSED], orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        createdAt
        reviews(last: 100) {
          nodes {
            author {
              login
            }
            createdAt
          }
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
"""

if __name__ == "__main__":
    assert token, "You must set GITHUB_PERSONAL_ACCESS_TOKEN environment variable"

    variables = {
        "repoOwner": "capitalrx",
        "repoName": "code.capitalrx.com",
        "after": None,
    }

    logins = []
    pr_created_at = arrow.now()
    while pr_created_at > START_DATE:
        resp = requests.post(
            'https://api.github.com/graphql',
            json={"query": query, "variables": variables},
            headers={"Authorization": f"Bearer {token}"}
        )

        body = resp.json()

        for pr_node in body['data']['repository']['pullRequests']['nodes']:
            pr_created_at = arrow.get(pr_node['createdAt'])
            for review_node in pr_node['reviews']['nodes']:
                if (
                    arrow.get(review_node['createdAt']) > START_DATE
                    and (login := review_node['author']['login']) in LOGIN_WHITELIST
                ):
                    logins.append(login)

        page_info = body['data']['repository']['pullRequests']['pageInfo']

        if not page_info['hasNextPage']:
            break

        variables["after"] = page_info['endCursor']

    rows = [(count, login) for login, count in Counter(logins).items()]
    rows.sort(reverse=True)
    rows = rows[:PLACES]

    for row in rows:
        print(row)
