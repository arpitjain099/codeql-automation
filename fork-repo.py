from github import Github
import os
import csv
import subprocess
import yaml

GITHUB_TOKEN = ""
GITHUB_USERNAME = "arpitjain799"

command = ['rm', '-rf', "clonerepo/test/"]
subprocess.run(command, check=True)

directory_name = "clonerepo/test/"
subprocess.call(["mkdir", "-p", directory_name])

# Open the CSV file
with open('clean_csv.csv') as csvfile:

	# Create a CSV reader object
	csvreader = csv.DictReader(csvfile)

	# Iterate over each row in the CSV file
	for row in csvreader:
		# Print each row
		if "github_url" in row.keys():
			print(row["github_url"])
			# Your personal access token or OAuth token
			
			# Owner and name of the repository you want to fork
			REPO_OWNER = row["github_url"].split("/")[-2]
			REPO_NAME = row["github_url"].split("/")[-1]


			# Clone the forked repository to your local machine
			#os.system(f"git clone https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git")

			# Authenticate with your GitHub account
			g = Github(GITHUB_TOKEN)

			# Fork the repository to your account
			repo = g.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
			default_branch = repo.default_branch
			branch = repo.get_branch(default_branch)
			"""
			default_branch = repo.default_branch
			branch = repo.get_branch(default_branch)
			protection_settings = {
				"required_status_checks": None,
				"enforce_admins": True,
				"restrictions": None
			}
			protection = repo.get_branch(default_branch).edit_protection(**protection_settings)
			"""
			
			#protection = branch.create_protection(required_status_checks=None, enforce_admins=True, restrictions=None)


			#branch.edit_protection(strict=True, enforce_admins=True, required_pull_request_reviews={})
			forked_repo = g.get_user().create_fork(repo)

			print(REPO_NAME)
			print()
			print()
			
			print("aaaaa")
			print(row["github_url"])
			try:
				subprocess.run(['git', 'clone', '--depth', '1', f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git", "clonerepo/test/"], check=True)
			except subprocess.CalledProcessError as e:
				print(f"Git clone failed " + f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git")
				continue

			#os.system(f"git clone https://github.com/f{GITHUB_USERNAME}/f{REPO_NAME}.git")
			# Add CodeQL code to the repository
			# Follow the CodeQL documentation to create a CodeQL analysis

			# Commit and push changes to the forked repository

			os.chdir("clonerepo/test/")
			directory_name = ".github"
			subprocess.call(["mkdir", "-p", directory_name])

			directory_name = ".github/workflows"
			subprocess.call(["mkdir", "-p", directory_name])

			command = ['rm', '-rf', ".github/workflows/codeql.yml"]
			subprocess.run(command, check=True)

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
					"fail-fast": False,
					"matrix": {
					"language": [
						"python"
					]
					}
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
						"languages": "${{ matrix.language }}",
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
			print(a["on"]["push"]["branches"])
			
			with open(".github/workflows/codeql.yml", "w") as f:
				yaml.dump(a, f)
			os.system("git add .")
			os.system("git commit -m 'Added CodeQL code'")
			subprocess.call(["git", "push", "origin", branch.name])
			print("Changes pushed to " + branch.name)

			"""
			pull_request = repo.create_pull(
				title=f"Feature branch merge (branch -> branch)",
				body="Automatically created and approved by script.",
				head=branch.name,
				base=branch.name
			)
			REVIEW_BODY = "Workflow runs approved"
			REVIEW_EVENT = "APPROVE"
			pull_request.create_review(body=REVIEW_BODY, event=REVIEW_EVENT)
			"""

			os.chdir("../../")
			command = ['rm', '-rf', "clonerepo/test/"]
			subprocess.run(command, check=True)
			current_dir = subprocess.check_output("pwd").decode().strip()
			print("current_dir: " + current_dir)