import os
import base64
import requests
import time
import re
import json
from backend import get_data_from_agent
from file_creator import create_project_structure

# GitHub credentials
GITHUB_USERNAME = "psudeoR3BEL"
GITHUB_TOKEN = "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"  # Replace with your actual token
REPO_NAME = "complexProject"
GITHUB_API = "https://api.github.com"
PAGES_API_URL = f"{GITHUB_API}/repos/{GITHUB_USERNAME}/{REPO_NAME}/pages"

# Agent API details (Modify if needed)
AGENT_API_URL = "https://api-lr.agent.ai/v1/agent/2kgl5xlfgopgbhgp/webhook/2255afc9"

# GitHub API URLs
REPO_API_URL = f"{GITHUB_API}/user/repos"
CONTENT_API_URL = f"{GITHUB_API}/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/"

# Function to get AI-generated HTML
def generate_html(prompt):
    headers = {"Content-Type": "application/json"}
    response = requests.post(AGENT_API_URL, json={"user_input": prompt}, headers=headers)

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
            print("⚠️ No HTML code found in the response.")
            return False
    else:
        print(f"⚠️ Error from AI Agent: {response.status_code}, {response.text}")
        return False

# Function to create GitHub repository (if it doesn't already exist)
def create_github_repo():
    # Try to fetch the repository info first
    repo_url = f"{GITHUB_API}/repos/{GITHUB_USERNAME}/{REPO_NAME}"
    repo_resp = requests.get(repo_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if repo_resp.status_code == 200:
        print(f"⚠️ Repository '{REPO_NAME}' already exists. Skipping creation.")
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
        print(f"⚠️ Error creating repository: {response.json()}")
        return False

# Function to upload index.html to GitHub (only if the file doesn't already exist)
def upload_file():
    if not os.path.exists("index.html"):
        print("⚠️ Error: index.html file not found in current directory")
        return False

    # Check if file already exists in the repo
    response = requests.get(CONTENT_API_URL+"index.html" + "?ref=main", headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if response.status_code == 200:
        print("⚠️ File 'index.html' already exists in the repo. Skipping upload.")
        return True

    # Otherwise, read and upload the file
    with open("index.html", "rb") as file:
        file_content = base64.b64encode(file.read()).decode("utf-8")
    file_data = {
        "message": "Upload index.html",
        "content": file_content,
        "branch": "main"
    }
    response = requests.put(CONTENT_API_URL+"index.html", json=file_data, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    if response.status_code == 201:
        print("✅ File 'index.html' uploaded successfully!")
        return True
    else:
        print("⚠️ Error uploading file:", response.json())
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
        print(f"⚠️ Error enabling GitHub Pages: {response.json()}")
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
    print("Agent payload:", json.dumps(payload_agent))
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
        print("⚠️ No HTML code found in the response.")

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


def hostMultiFiles(dirName, current_path=""):
    """
    Upload multiple files maintaining directory structure
    
    Args:
        dirName: Root directory to upload
        current_path: Current path within the repository
    """
    try:
        # Create repo only once at the start
        if not current_path:
            create_github_repo()
            
        for item in os.listdir(dirName):
            full_path = os.path.join(dirName, item)
            repo_path = os.path.join(current_path, item).replace("\\", "/")
            
            if os.path.isfile(full_path):
                try:
                    print(f"Uploading {repo_path}...")
                    handleFileUpload(full_path, repo_path)
                except Exception as e:
                    print(f"Error uploading {repo_path}: {str(e)}")
            else:
                # Recursively handle subdirectories
                hostMultiFiles(full_path, repo_path)
        return True        
    except Exception as e:
        print(f"Error processing directory {dirName}: {str(e)}")
        return False

# Modified handleFileUpload to support paths
def handleFileUpload(local_file_path, repo_path):
    """
    Upload a single file to the repository
    
    Args:
        local_file_path: Path to file on local system
        repo_path: Path where file should be stored in repository
    """
    content_url = f"{GITHUB_API}/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{repo_path}"
    
    # Check if file exists
    response = requests.get(
        content_url, 
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )
    
    if response.status_code == 200:
        print(f"⚠️ File '{repo_path}' already exists in the repo. Skipping upload.")
        return True

    # Read and upload the file
    try:
        with open(local_file_path, "rb") as file:
            file_content = base64.b64encode(file.read()).decode("utf-8")
            
        file_data = {
            "message": f"Upload {repo_path}",
            "content": file_content,
            "branch": "main"
        }
        
        response = requests.put(
            content_url, 
            json=file_data, 
            auth=(GITHUB_USERNAME, GITHUB_TOKEN)
        )
        
        if response.status_code == 201:
            print(f"✅ File '{repo_path}' uploaded successfully!")
            return True
        else:
            print(f"⚠️ Error uploading file {repo_path}:", response.json())
            return False
            
    except Exception as e:
        print(f"⚠️ Error reading/uploading file {local_file_path}: {str(e)}")
        return False


def getDataFromAgent():
    res=  requests.post('https://api-lr.agent.ai/v1/agent/bzj3gxj532k08keq/webhook/b2c20880',json={
        "user_input":"hey developer create a slider animtion website for me basically its a landing page for my upcoming resturant in slider show different foods using svg icons"
    },headers={"Content-Type": "application/json"}).json()
    data = res['response']
    projDir = data['project dir'].split('\n')
    print(projDir)
    lst = [data['cssDesc'],data['htmlDesc'],data['jsDesc']]
    compeleteCode = ''
    for eli in lst:
        res = requests.post('https://api-lr.agent.ai/v1/agent/mfs3r5zucxquymkj/webhook/017c1ac3',json={
            "user_input":eli
        },headers={"Content-Type": "application/json"}).json()
        compeleteCode+= res['response']
    res = requests.post('https://api-lr.agent.ai/v1/agent/qv7ehw6pblvfpb20/webhook/3d4841e6',json={
        "user_input": compeleteCode
    },headers={"Content-Type": "application/json"}).json()
    dirMap = {}
    for dir in projDir:
        dirComp = dir.split('/') #components of the dir
        fileName = dirComp[len(dirComp)-1].split('.')[0]
        fileExt = dirComp[len(dirComp)-1].split('.')[1]
        if fileExt == 'html':
            dirMap[dir] = res['response']['html'][f'{fileName}.{fileExt}']
        elif fileExt == 'css':
            dirMap[dir] = res['response']['css'][f'{fileName}.{fileExt}']
        elif fileExt == 'js':
            dirMap[dir] = res['response']['js'][f'{fileName}.{fileExt}']
        print(dirMap)



   
      

     


# 🚀 Execute the complete workflow
if __name__ == "__main__":
    user_prompt = '''
    Design a dark, modern landing page for a forward-thinking business that exudes sophistication and innovation. The page should feature a sleek, minimalist layout with a deep charcoal or black background, accented by vibrant colors (like neon blue or electric orange) for key elements such as buttons and highlights. Include the following sections:

Hero Section: A bold headline with a captivating subheadline, and a clear, prominent call-to-action button.
About/Services: A brief overview of the business offerings, using modern icons and concise text to communicate value.
Testimonials: A section showcasing client testimonials in a carousel or grid layout.
Contact/Footer: A simple contact form alongside social media links and essential business information.
Ensure the design is responsive and mobile-friendly, uses modern typography, and incorporates smooth transitions or interactive elements to enhance user engagement. The overall aesthetic should be both minimal and impactful, reflecting the innovative nature of the business.
'''
    file_data = get_data_from_agent(user_prompt)
    if file_data:
        success = create_project_structure(file_data)
        if success:
            from githubHandler import main
            main()
    # enable_github_pages()


