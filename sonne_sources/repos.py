import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import time

# Replace 'your_github_username' with your actual GitHub username
GITHUB_USERNAME = 'MarkCarsonDev'
# Optionally, you can set a GitHub token for authenticated requests
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


def fetch_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    headers = {}
    if GITHUB_TOKEN:
        print("Using token")
        # wait for 5 seconds
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    params = {
        'sort': 'updated',
        'direction': 'desc',
        'per_page': 100  # Adjust as needed
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def fetch_repo_details(repo_full_name):
    url = f'https://api.github.com/repos/{repo_full_name}'
    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_commit_count(repo_full_name):
    url = f'https://api.github.com/repos/{repo_full_name}/commits'
    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    params = {'per_page': 1}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    # GitHub API returns a 'Link' header with pagination info
    if 'Link' in response.headers:
        link_header = response.headers['Link']
        # Extract the total number of pages from the last page URL
        if 'last' in link_header:
            last_page = link_header.split(',')[-1]
            total_pages = int(last_page.split('page=')[-1].split('>')[0])
            return total_pages
    return len(response.json())

def main():
    repos_data = fetch_repos(GITHUB_USERNAME)
    repos_list = []
    for repo in repos_data:
        repo_full_name = repo['full_name']
        repo_details = fetch_repo_details(repo_full_name)
        commit_count = fetch_commit_count(repo_full_name)
        repo_info = {
            'title': repo['name'],
            'description': repo['description'] or '',
            'url': repo['html_url'],
            'lines_committed': commit_count,  # Approximation
            'date': repo['updated_at'],
            # You can add more fields if needed
        }
        repos_list.append(repo_info)

    # Now create the sonne variable
    sonne_var('repos', repos_list)

    import json
    sonne_var('repos_json', json.dumps(repos_list))

main()
