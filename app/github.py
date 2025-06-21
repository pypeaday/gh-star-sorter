import os
import requests
import logging

def get_starred_repos():
    logging.info("Fetching starred repos from GitHub...")
    """Fetches all starred repositories for the authenticated user."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set")

    headers = {"Authorization": f"token {token}"}
    starred_repos = []
    page = 1
    while True:
        logging.info(f"Fetching page {page} of starred repos...")
        response = requests.get(
            f"https://api.github.com/user/starred?page={page}&per_page=100",
            headers=headers
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        if not data:
            break
        starred_repos.extend(data)
        page += 1
    
    logging.info(f"Found {len(starred_repos)} total starred repos.")
    return starred_repos
