import requests

GITHUB_TOKEN = input("Enter your github token: ")
GITHUB_USER = input("Enter your GitHub username: ")
repo_name = input("Enter a repo name: ")
while(len(repo_name) == 0):
    repo_name = input("Please enter a valid repo name: ")

url = "https://api.github.com/user/repos"
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
data = {"name": repo_name, "private": False}

response = requests.post(url, json=data, headers=headers)
if response.status_code == 201:
    print(f"Repository '{repo_name}' created successfully!")
elif response.status_code == 200:
    print(f"Repository '{repo_name}' already exists.")
    
else:
    print(f"Error: {response.json()}")
