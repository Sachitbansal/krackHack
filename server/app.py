import os
import base64
import requests
import re
import json
from dotenv import load_dotenv
load_dotenv()

# GitHub credentials
GITHUB_USERNAME = "psudeoR3BEL"
# this github ka access wlaa ttt tha
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "hello-world-site14"
# Agent API details (Modify if needed)
INITIAL_AGENT_API_URL = "https://api-lr.agent.ai/v1/agent/2kgl5xlfgopgbhgp/webhook/2255afc9"
MULTIFILECREATOR_AGENT_API_URL = "https://api-lr.agent.ai/v1/agent/qv7ehw6pblvfpb20/webhook/3d4841e6"

# GitHub API URLs
GITHUB_API = "https://api.github.com"
REPO_API_URL = f"{GITHUB_API}/user/repos"
CONTENT_API_URL = f"{GITHUB_API}/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/index.html"
PAGES_API_URL = f"{GITHUB_API}/repos/{GITHUB_USERNAME}/{REPO_NAME}/pages"

import os
import json
from typing import Dict
import os
import json
from typing import Dict

def create_project_structure(file_data: Dict[str, Dict[str, str]], project_name: str = "testProject") -> bool:
    """
    Create project structure from the provided file data
    
    Args:
        file_data: Dictionary containing file types and their contents
        project_name: Name of the project directory (default: 'testProject')
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create the main project directory if it doesn't exist
        os.makedirs(project_name, exist_ok=True)
        
        # Get the working directory content and clean it
        dir_content = file_data['workingDir']
        
        for dir_path, files in dir_content.items():
            # Handle both string and list inputs
            if isinstance(files, str):
                files_list = [f.strip() for f in files.split(',')]
            elif isinstance(files, list):
                files_list = [f.strip() for f in files]
            else:
                print(f'Unsupported type for files in {dir_path}: {type(files)}')
                continue
            
            # Create full directory path
            full_dir_path = os.path.join(project_name, dir_path.strip('/'))
            os.makedirs(full_dir_path, exist_ok=True)
            
            # Process each file
            for file in files_list:
                file = file.strip()
                if not file:
                    continue
                    
                # Get file extension and content
                file_ext = file.split('.')[-1]
                file_path = os.path.join(full_dir_path, file)
                
                # Write content if it exists in the corresponding type dictionary
                if file_ext in file_data and file in file_data[file_ext]:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(file_data[file_ext][file])
                else:
                    # Create empty file for images or other files without content
                    with open(file_path, 'w', encoding='utf-8') as f:
                        pass
                    print(f'Created empty file: {file} (no content provided in data)')
        
        return True
        
    except Exception as e:
        print(f'Error creating project structure: {str(e)}')
        return False
    



# Function to get AI-generated HTML
def generate_html(prompt):
    headers = {"Content-Type": "application/json"}
    response = requests.post(INITIAL_AGENT_API_URL, json={"user_input": prompt}, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        match = re.search(r'(<html[\s\S]*?</html>)', response_data.get('response', ''), re.DOTALL)
        if match:
            html_code = match.group(1)
            with open("index.html", "w", encoding="utf-8") as file:
                file.write(html_code)
            print("✅ HTML code successfully saved to index.html!")
            return True
        else:
            print("⚠ No HTML code found in the response.")
            return False
    else:
        print(f"⚠ Error from AI Agent: {response.status_code}, {response.text}")
        return False
    
def generate_html2o(prompt):
    headers = {"Content-Type": "application/json"}
    genresponse = requests.post("https://api-lr.agent.ai/v1/agent/z3m4lvnfzx38z4iu/webhook/9704cb2b", json={"user_input": prompt}, headers=headers).json()
    response = requests.post(INITIAL_AGENT_API_URL, json={"user_input": genresponse['response']}, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        # print(response_data)
        # match = re.search(r'(<html[\s\S]*?</html>)', response_data.get('response', ''), re.DOTALL)
        if True:
            # html_code = match.group(1)
            # print(response_data.get('response', ''))
            with open("output.txt", "w", encoding="utf-8") as file:
                file.write(response_data.get('response', ''))
            print("✅ HTML code successfully saved to index.html!")
            return True
        else:
            print("⚠ No HTML code found in the response.")
            return False
    else:
        print(f"⚠ Error from AI Agent: {response.status_code}, {response.text}")
        return False
    
    
    
def extract_code_blocks(text):
    pattern = re.findall(r"\n([\w\-/.]+)\n([\s\S]+?)", text)
    print(pattern)
    return pattern

def save_code_files(text):
    code_blocks = extract_code_blocks(text)
    for file_path, code in code_blocks:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create directories if not exist
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(code.strip() + "\n")  # Save code to the respective file
        print(f"Saved: {file_path}")
    
# Function to get AI-generated HTML
def multifileCreator(path='output.txt'):
    
    def read_file_to_variable(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

    text_content = read_file_to_variable(path)
    print('----------------the text content is :-------------------------------')
    print(text_content)
    headers = {"Content-Type": "application/json"}
    response = requests.post(MULTIFILECREATOR_AGENT_API_URL, json={"user_input": text_content}, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        print(response_data['response'])
        # match = re.search(r'(<html[\s\S]*?</html>)', response_data.get('response', ''), re.DOTALL)
        if True:
            # html_code = match.group(1)
            if(create_project_structure(response_data.get('response', ''),'testProject')):

                print("✅ HTML code successfully saved to index.html!")
                return response_data.get('response', '')
            return 'error in the html code'

    else:
        print(f"⚠ Error from AI Agent: {response.status_code}, {response.text}")
        return False

# Function to create GitHub repository (if it doesn't already exist)
def create_github_repo():
    # Try to fetch the repository info first
    repo_url = f"{GITHUB_API}/repos/{GITHUB_USERNAME}/{REPO_NAME}"
    repo_resp = requests.get(repo_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if repo_resp.status_code == 200:
        print(f"⚠ Repository '{REPO_NAME}' already exists. Skipping creation.")
        return True

    # Otherwise, create the repo
    repo_data = {
        "name": REPO_NAME,
        "description": "A simple Hello World website",
        "private": False,
        "auto_init": True  # Initializes repo with README
    }
    response = requests.post(REPO_API_URL, json=repo_data, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    if response.status_code == 201:
        print(f"✅ Repository '{REPO_NAME}' created successfully!")
        return True
    else:
        print(f"⚠ Error creating repository: {response.json()}")
        return False

# Function to upload index.html to GitHub (only if the file doesn't already exist)
def upload_file():
    if not os.path.exists("index.html"):
        print("⚠ Error: index.html file not found in current directory")
        return False

    # Check if file already exists in the repo
    response = requests.get(CONTENT_API_URL + "?ref=main", headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if response.status_code == 200:
        print("⚠ File 'index.html' already exists in the repo. Skipping upload.")
        return True

    # Otherwise, read and upload the file
    with open("index.html", "rb") as file:
        file_content = base64.b64encode(file.read()).decode("utf-8")
    file_data = {
        "message": "Upload index.html",
        "content": file_content,
        "branch": "main"
    }
    response = requests.put(CONTENT_API_URL, json=file_data, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    if response.status_code == 201:
        print("✅ File 'index.html' uploaded successfully!")
        return True
    else:
        print("⚠ Error uploading file:", response.json())
        return False

# Function to enable GitHub Pages
def enable_github_pages():
    pages_data = {
        "source": {
            "branch": "main",
            "path": "/"
        }
    }
    response = requests.post(PAGES_API_URL, json=pages_data, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    if response.status_code in [201, 204]:
        print(f"✅ GitHub Pages enabled for {REPO_NAME}!")
        print(f"🔗 Your website will be available soon at: https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/")
        return True
    else:
        print(f"⚠ Error enabling GitHub Pages: {response.json()}")
        return False

# Function to modify the structure of the file and push changes to GitHub
def modifyStructure(inputFile, modificationPrompt):
    # Read the local file content
    with open(inputFile, 'r', encoding='utf-8') as f:
        file_text = f.read()
    payload_agent = {
        "code": file_text,
        "user_input": modificationPrompt,
    }
    # print("Agent payload:", json.dumps(payload_agent))
    # Call the agent API for modifications
    res = requests.post('https://api-lr.agent.ai/v1/agent/6k2sqi0lpawbgasb/webhook/85e8f0af',
                        json=payload_agent,
                        headers={"Content-Type": "application/json"})
    print("Agent response:", res)
    data = res.json()
    match = re.search(r'(<html[\s\S]*?</html>)', data.get('response', ''), re.DOTALL)
    if match:
        html_code = match.group(1)
        with open(inputFile, "w", encoding="utf-8") as file:
            file.write(html_code)
        print(f"✅ HTML code successfully saved to {inputFile}!")
    else:
        print("⚠ No HTML code found in the response.")

    # Get the remote file from GitHub
    url = f"{GITHUB_API}/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{inputFile}?ref=main"
    repoData = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"}).json()

    # If the file exists on GitHub, decode its content and get the SHA; otherwise, set as None.
    if "content" in repoData:
        remote_content_encoded = repoData["content"].replace("\n", "")
        remote_content = base64.b64decode(remote_content_encoded).decode("utf-8")
    else:
        remote_content = None
    remote_sha = repoData.get("sha")

    # Read the modified local content
    with open(inputFile, 'r', encoding='utf-8') as f:
        local_content = f.read()

    # If the file exists remotely and contents are identical, skip the update.
    if remote_content is not None and local_content == remote_content:
        print("No changes detected; nothing to push.")
        return False
    else:
        # Encode local content in base64
        content_bytes = local_content.encode("utf-8")
        b64_content = base64.b64encode(content_bytes).decode("utf-8")
    
        # Prepare payload for updating (or creating) the file
        payload = {
            "message": modificationPrompt,
            "content": b64_content,
            "branch": "main"
        }
        if remote_sha:
            payload["sha"] = remote_sha

        # Update URL (note: use inputFile, not an undefined variable)
        update_url = f"{GITHUB_API}/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{inputFile}"
        update_response = requests.put(update_url,
                                       headers={"Authorization": f"token {GITHUB_TOKEN}"},
                                       json=payload)
    
        if update_response.status_code in [200, 201]:
            print("File updated successfully on GitHub.")
            return True
        else:
            print("Failed to update file. Response:")
            print(update_response.json())
            return False
        

def makeChangesOnTheCode(jsonOfTheCode,prompt):
    try:
        jsonStr = json.dumps(jsonOfTheCode)
        res = requests.post('https://api-lr.agent.ai/v1/agent/66lf38xw0ztxs00a/webhook/e02d5dba',
                            json={
                                "user_input":jsonStr,
                                "query":prompt
                            },headers={"Content-Type": "application/json"}).json()
        data = res['response']
        if create_project_structure(data,"testProject"):
            return True
    except Exception as e:
        print(e)
        
