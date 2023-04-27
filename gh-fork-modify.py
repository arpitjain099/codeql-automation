from os import access
import requests
import base64
from github import Github
import time
import sys
import csv

def reverse_timer(seconds):
	for second in range(seconds, 0, -1):
		print(f"Time left: {second} seconds", end="\r")
		time.sleep(1)

unique_gh = []
with open('clean_csv.csv') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		if "github_url" in row.keys() and row["github_url"] != "":
			if row["github_url"] not in unique_gh:
				unique_gh.append(row["github_url"])

print(len(unique_gh))

codeql_file_path = "codeql.yml"
file_name = "codeql.yml"
fork_owner = "arpitjain799"
access_token = ""
folder_path = ".github/workflows/"

for gh_url in unique_gh:
	print()
	print(gh_url)
	owner = gh_url.split("/")[-2]
	repo = gh_url.split("/")[-1]
	fork_repo = f"{owner}-{repo}"

	g = Github(access_token)
	repo_original = g.get_repo(f"{owner}/{repo}")
	g.get_user().create_fork(repo_original)

	repo_t = g.get_repo(f"{fork_owner}/{repo}")
	time.sleep(5)
	default_branch = repo_t.default_branch
	branch = repo_t.get_branch(default_branch)
	default_branch = branch.name
	flag_github_exists = False
	flag_workflow_exists = False

	parent_folder = requests.get(f"https://api.github.com/repos/{fork_owner}/{repo}/contents/", headers={'Accept': 'application/vnd.github+json','Authorization': f"Bearer {access_token}",	'X-GitHub-Api-Version': '2022-11-28'})
	#print(parent_folder.json())
	for i in parent_folder.json():
		if i["path"] == ".github":
			#print("github entry")
			flag_github_exists = True
			workflow_folder = requests.get(f"https://api.github.com/repos/{fork_owner}/{repo}/contents/.github/", headers={'Accept': 'application/vnd.github+json','Authorization': f"Bearer {access_token}",	'X-GitHub-Api-Version': '2022-11-28'})
			#b = repo_t.get_contents(".github/")
			#print(workflow_folder.json())
			for j in workflow_folder.json():
				if j["path"] == ".github/workflows":
					flag_workflow_exists = True
					#print("workflows entry")
					#contents = repo_t.get_contents(".github/workflows/")
					file_list = requests.get(f"https://api.github.com/repos/{fork_owner}/{repo}/contents/.github/workflows/", headers={'Accept': 'application/vnd.github+json','Authorization': f"Bearer {access_token}",	'X-GitHub-Api-Version': '2022-11-28'})

					#print(file_list.json())
					for content_file in file_list.json():
						if content_file["type"] == "file":
							#content_file = repo_t.get_contents(".github/workflows/content_file")
							#print(content_file.path)
							#print(content_file.sha)
							#print(default_branch)
							#repo_t.delete_file(content_file.path, "Delete file", content_file.sha, branch=default_branch) #: {str(content_file.path)}
							file_path = content_file["path"]
							delete_response = requests.delete(f"https://api.github.com/repos/{fork_owner}/{repo}/contents/{file_path}", headers={"Authorization": f"token {access_token}"}, json={"message": f"Delete {file_path}", "sha": content_file["sha"], "branch": default_branch})
							
							if delete_response.status_code == 200:
								print(f"Deleted {file_path}")
							else:
								print(f"Error deleting {file_path}: {delete_response.content}")
							flag_github_exists = False
							flag_workflow_exists = False
					break
			break
	
	with open(codeql_file_path, "r") as file:
		file_content = file.read()
	try:
		repo_t.create_file(f"{folder_path}{file_name}", "Add new file", file_content, branch=default_branch)
		print(f"File {file_name} added successfully to folder path/to/folder")
	except Exception as e:
		print(f"Error creating file: {e}")
	reverse_timer(10)

"""
if flag_workflow_exists == False and flag_github_exists == False:
	try:
		repo.create_file(f".github/", "Create folder", "", branch=default_branch)
	except Exception as e:
		print(f"Folder .github/ already exists: {e}")

	try:
		repo.create_file(f".github/workflows/", "Create folder", ".github", branch=default_branch)
	except Exception as e:
		print(f"Folder .github/workflows/ already exists: {e}")

if flag_workflow_exists == False and flag_github_exists == True:
	try:
		repo.create_file(f".github/workflows/", "Create folder", "", branch=default_branch)
	except Exception as e:
		print(f"Folder .github/workflows/ already exists: {e}")
"""
"""
with open(codeql_file_path, "rb") as file:
	file_content = file.read()
encoded_content = base64.b64encode(file_content)
"""

"""
file_content = "This is a new file"
try:
	repo.create_file(f"{folder_path}/{file_name}", "Add new file", file_content, branch=default_branch)
	print(f"File {file_name} added successfully to folder {folder_path}")
except Exception as e:
	print(f"Error creating file: {e}")
"""

"""
# delete all files in .github/workflows folder
headers = {
	'Accept': 'application/vnd.github+json',
	'Authorization': f"Bearer {access_token}",
	'X-GitHub-Api-Version': '2022-11-28',
}

response = requests.get(f"https://api.github.com/repos/{fork_owner}/{repo}/contents/.github/workflows", headers=headers)
response = response.json()

# Check the response status code and parse the response JSON
if response.status_code == 200:
	subdir_data = response.json()
	# Delete all files inside the subdirectory
	for item in subdir_data:
		item_path = item["path"]
		item_sha = item["sha"]
		
		delete_response = requests.delete(f"https://api.github.com/repos/{fork_owner}/{repo}/contents/{item_path}", headers={"Authorization": f"token {access_token}"}, json={"message": f"Delete {item_path}", "sha": item_sha, "branch": default_branch})
		
		if delete_response.status_code == 200:
			print(f"Deleted {item_path}")
		else:
			print(f"Error deleting {item_path}: {delete_response.content}")
else:
	sys.exit(f"Subdirectory .github/workflows does not exist or cannot be accessed.")
	
	# Create the .github/workflows directory
	create_dir_response = requests.put(f"https://api.github.com/repos/{fork_owner}/{repo}/contents/{subdir_path}", headers={ "Authorization": f"token {access_token}"}, json={"message": f"Create {subdir_path}", "content": "", "branch": default_branch})
	
	if create_dir_response.status_code == 201:
		print(f"Created {subdir_path}")
	else:
		print(f"Error creating {subdir_path}: {create_dir_response.content}")

# Define the API endpoint and request headers
url = f"https://api.github.com/repos/{fork_owner}/{fork_repo}/contents/{subdir_path}/code.yml"
headers = {
	"Authorization": "token your-personal-access-token",
	"Content-Type": "application/json"
}

# Define the API endpoint and request headers
url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
headers = {
	"Authorization": "token your-personal-access-token",
	"Content-Type": "application/json"
}

# Encode the content of the file in Base64 format
content = base64.b64encode(b"Hello, world!").decode("utf-8")

# Define the request body
data = {
	"message": "Add newfile.txt",
	"content": content,
	"branch": default_branch
}

# Send a PUT request to create the new file
response = requests.put(url, headers=headers, json=data)

# Check the response status code
if response.status_code == 201:
	print("New file created successfully!")
	
	# Get the SHA of the newly created file
	response_json = response.json()
	file_sha = response_json["content"]["sha"]
	
	# Define the request body for creating a new commit
	commit_data = {
		"message": "Add newfile.txt",
		"content": content,
		"sha": file_sha
	}
	
	# Send a POST request to create a new commit
	commit_response = requests.post(f"https://api.github.com/repos/{owner}/{repo}/git/commits", headers=headers, json=commit_data)
	
	# Check the response status code for the commit request
	if commit_response.status_code == 201:
		print("Commit created successfully!")
	else:
		print("Error creating commit:", commit_response.content)
else:
	print("Error creating new file:", response.content)
"""

"""
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/arpitjain799/accelerate/actions/workflows

curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/arpitjain799/accelerate/actions/workflows/55416481/dispatches \
  -d '{"ref":"main","inputs":{"name":"Mona the Octocat","home":"San Francisco, CA"}}'

curl -L \
  -X GET \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/arpitjain799/bb-ki-slotting/contents/

curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/arpitjain799/accelerate/contents/.github/workflows

/repos/github/docs/contents/rest/reference/users?ref=main

"""