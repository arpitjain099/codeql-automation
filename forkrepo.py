from github import Github
import os
import csv
import subprocess
import yaml
import time

GITHUB_TOKEN = ""
GITHUB_USERNAME = "arpitjain799"

command = ['rm', '-rf', "clonerepo/test/"]
subprocess.run(command, check=True)

directory_name = "clonerepo/test/"
subprocess.call(["mkdir", "-p", directory_name])
unique_gh = []
# Open the CSV file
with open('clean_csv.csv') as csvfile:

	# Create a CSV reader object
	csvreader = csv.DictReader(csvfile)

	# Iterate over each row in the CSV file
	for row in csvreader:
		if "github_url" in row.keys() and row["github_url"] != "":
			if row["github_url"] not in unique_gh:
				unique_gh.append(row["github_url"])

print(len(unique_gh))

for gh_url in unique_gh:
	print()
	print("aaaaa")
	print(gh_url)

	REPO_OWNER = gh_url.split("/")[-2]
	REPO_NAME = gh_url.split("/")[-1]

	# Authenticate with your GitHub account
	g = Github(GITHUB_TOKEN)
	# Fork the repository to your account
	repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
	g.get_user().create_fork(repo)
	time.sleep(5)
	default_branch = repo.default_branch
	branch = repo.get_branch(default_branch)

	try:
		subprocess.run(['git', 'clone', '--depth', '1', f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git", "clonerepo/test/"], check=True)
	except subprocess.CalledProcessError as e:
		print(f"Git clone failed " + f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git")
		continue

	os.chdir("clonerepo/test/")
	"""
	directory_name = ".github"
	subprocess.call(["mkdir", "-p", directory_name])

	directory_name = ".github/workflows"
	subprocess.call(["mkdir", "-p", directory_name])

	command = ['rm', '-rf', ".github/workflows/*"]
	subprocess.run(command, check=True)
	"""
	new_directory = ".github"
	# Create the directory and its parent directories if needed
	os.makedirs(new_directory, exist_ok=True)

	#directory_name = ".github"
	#subprocess.run(["mkdir", "-p", directory_name])

	new_directory = ".github/workflows"
	# Create the directory and its parent directories if needed
	os.makedirs(new_directory, exist_ok=True)

	#directory_name = ".github/workflows"
	#subprocess.run(["mkdir", "-p", directory_name])

	#command = "rm -rf .github/workflows/*"
	#subprocess.run(command, check=True)

	# Define the path to the subfolder
	subfolder_path = ".github/workflows/"

	# Check if the subfolder exists
	if os.path.exists(subfolder_path) and os.path.isdir(subfolder_path):
		# Iterate over the files in the subfolder
		for file_name in os.listdir(subfolder_path):
			file_path = os.path.join(subfolder_path, file_name)
			# Check if it's a regular file
			if os.path.isfile(file_path):
				try:
					# Remove the file
					os.remove(file_path)
					print(f"File {file_path} has been deleted.")
				except OSError as e:
					print(f"Error deleting file {file_path}: {e}")
	else:
		print("The specified subfolder does not exist or is not a directory.")

	#subprocess.call(["cp", "/Users/arpitjain/Downloads/codeql-security/codeql.yml", ".github/workflows/codeql.yml"])
	
	a = {
	"name": "CodeQL",
	"on": {
		"push": {
		"branches": []
		}
	},
	"jobs": {
		"analyze": {
		"name": "Analyze",
		"runs-on": "ubuntu-latest",
		"permissions": {
			"actions": "read",
			"contents": "read",
			"security-events": "write"
		},
		"strategy": {
			"fail-fast": False
		},
		"steps": [
			{
			"name": "Checkout repository",
			"uses": "actions/checkout@v3"
			},
			{
			"name": "Initialize CodeQL",
			"uses": "github/codeql-action/init@v2",
			"with": {
				"languages": "python",
				"queries": "security-and-quality"
			}
			},
			{
			"name": "Autobuild",
			"uses": "github/codeql-action/autobuild@v2"
			},
			{
			"name": "Perform CodeQL Analysis",
			"uses": "github/codeql-action/analyze@v2"
			}
		]
		}
	}
	}
	a["on"]["push"]["branches"].append(branch.name)
	
	with open(".github/workflows/codeql.yml", "w") as f:
		yaml.dump(a, f)
	os.system("git add .")
	os.system("git commit -m 'Added CodeQL code'")
	subprocess.call(["git", "push", "origin", branch.name])
	print("Changes pushed to " + branch.name)

	os.chdir("../../")
	command = ['rm', '-rf', "clonerepo/test/"]
	subprocess.run(command, check=True)