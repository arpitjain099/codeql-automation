import requests
import base64
import json
owner = "arpitjain799"
repo = "frozenlist"
path_to_file = "code.yml"

# Set the API endpoint URLs
file_url = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"
commit_url = "https://api.github.com/repos/{owner}/{repo}/git/commits"
access_token = ""
# Set the API headers and parameters
headers = {"Authorization": f"token {access_token}", "Content-Type": "application/json"}


url = f'https://api.github.com/repos/{owner}/{repo}/contents/'
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get(url, headers=headers)
response_json = json.loads(response.text)
sha = response_json[0]['sha']

"""
message = 'Delete .github/workflows folder'
url = f'https://api.github.com/repos/{owner}/{repo}/contents/.github/workflows'

data = {'message': message, 'sha': sha}
response = requests.delete(url, headers=headers, data=json.dumps(data))
if response.status_code == 200:
	print('Folder deleted successfully')
else:
	print(f'Error deleting folder: {response.text}')
"""

# Delete all the files in the folder
url = f'https://api.github.com/repos/{owner}/{repo}/contents/.github/workflows'
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get(url, headers=headers)
response_json = json.loads(response.text)
print(response_json)

for file in response_json:
	# Check if the file is a directory
	print(file)
	if file['type'] == 'dir':
		print(f'Skipping directory {file["name"]}')
		continue

	# Set the commit message and request URL for each file
	message = f'Delete {file["name"]}'
	url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file["path"]}'

	# Get the SHA hash of the last commit that modified the file
	sha = file['sha']

	# Make the DELETE request to delete the file
	data = {'message': message, 'sha': sha}
	response = requests.delete(url, headers=headers, data=json.dumps(data))
	if response.status_code == 200:
		print(f'File {file["name"]} deleted successfully')
	else:
		print(f'Error deleting file {file["name"]}: {response.text}')

# add .github folder
content = ''.encode('utf-8')
encoded_content = base64.b64encode(content).decode('utf-8')
message = 'Create new folder'
url = f'https://api.github.com/repos/{owner}/{repo}/contents/.github/'

# Make the PUT request to create the new file
data = {'message': message, 'content': encoded_content}
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.put(url, headers=headers, data=json.dumps(data))

if response.status_code == 201:
	print('New folder created successfully')
else:
	print(f'Error creating new folder: {response.text}')
	
# add .github/workflows folder
content = ''.encode('utf-8')
encoded_content = base64.b64encode(content).decode('utf-8')
message = 'Create new folder'
url = f'https://api.github.com/repos/{owner}/{repo}/contents/.github/workflows'

# Make the PUT request to create the new file
data = {'message': message, 'content': encoded_content}
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.put(url, headers=headers, data=json.dumps(data))

if response.status_code == 201:
	print('New folder created successfully')
else:
	print(f'Error creating new folder: {response.text}')

"""
folder_name = '.github'
folder_content = base64.b64encode(f'{folder_name}/'.encode('utf-8')).decode('utf-8')

message = 'Add new folder'
url = f'https://api.github.com/repos/{owner}/{repo}/contents/.github'

data = {'message': message, 'content': folder_content}
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.put(url, headers=headers, data=json.dumps(data))

if response.status_code == 201:
	print('New folder created successfully')
else:
	print(f'Error creating new folder: {response.text}')
"""

"""
folder_name = 'workflows'
folder_content = base64.b64encode(f'{folder_name}/'.encode('utf-8')).decode('utf-8')

message = 'Add new folder'
url = f'https://api.github.com/repos/{owner}/{repo}/contents/.github/{path}'

data = {'message': message, 'content': folder_content}
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.put(url, headers=headers, data=json.dumps(data))

if response.status_code == 201:
	print('New folder created successfully')
else:
	print(f'Error creating new folder: {response.text}')

"""

"""
payload = {"message": "Add code.yml", "committer": {"name": "Arpit Jain", "email": "arpitjain799@gmail.com"}, "sha": "bXkgbmV3IGZpbGUgY29udGVudHM"}

# Read the contents of the file and encode to base64
with open(path_to_file, "rb") as file:
	encoded_file_content = base64.b64encode(file.read()).decode()

# Set the file API endpoint URL with parameters
file_url = file_url.format(owner=owner, repo=repo, path=path_to_file)

# Set the file API payload
file_payload = {"message": "adding code.yml", "content": encoded_file_content}

# Make the API call to create the file
response = requests.put(file_url, headers=headers, json=file_payload)

# Get the response data and commit SHA
print(response)
response_data = response.json()

print()
print(response_data)
commit_sha = response_data["commit"]["sha"]

# Set the commit API endpoint URL
commit_url = commit_url.format(owner=owner, repo=repo)

# Set the commit API payload with the commit SHA and file content
payload["sha"] = commit_sha
payload["content"] = encoded_file_content

# Make the API call to commit the changes
response = requests.post(commit_url, headers=headers, json=payload)

# Print the response status code
print(response.status_code)
"""