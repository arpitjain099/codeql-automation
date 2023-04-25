import requests
from requests.auth import HTTPBasicAuth

# Replace these with your own values
username = "arpitjain799"
personal_access_token = "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"

# Define the API endpoints
base_url = "https://api.github.com"
user_repos_endpoint = f"{base_url}/user/repos?per_page=100&page="

for i in range(1, 3):
	# Get a list of user repositories
	response = requests.get(user_repos_endpoint + str(i), auth=HTTPBasicAuth(username, personal_access_token))
	repos = response.json()
	print(len(repos))

	# Iterate through repositories and check for the presence of a .github/workflows directory
	repos_without_workflows = []
	for repo in repos:
		repo_name = repo["name"]
		repo_owner = repo["owner"]["login"]
		workflows_url = f"{base_url}/repos/{repo_owner}/{repo_name}/contents/.github/workflows"

		workflows_response = requests.get(workflows_url, auth=HTTPBasicAuth(username, personal_access_token))
		if workflows_response.status_code == 404:  # Not found
			repos_without_workflows.append(repo_name)

	# Print repositories without workflows
	print("Repositories without workflows:")
	for repo in repos_without_workflows:
		print(repo)
