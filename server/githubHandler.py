import os
import base64
import requests
import logging
from typing import List, Optional
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_repo_contents(github_token: str, username: str, repo_name: str, path: str = "") -> bool:
    """
    Delete all contents of a GitHub repository recursively
    
    Args:
        github_token: GitHub personal access token
        username: GitHub username
        repo_name: Repository name
        path: Current path within the repository
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get contents of current path
        contents_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{path}"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.get(contents_url, headers=headers)
        response.raise_for_status()
        
        contents = response.json()
        
        # Handle empty repository or directory
        if not contents:
            logger.info(f"Path {path} is empty")
            return True
            
        # Handle case where contents is a single file (not a list)
        if not isinstance(contents, list):
            contents = [contents]
            
        # Delete each item
        for item in contents:
            item_path = item['path']
            
            # Recursively delete directories
            if item['type'] == 'dir':
                if not delete_repo_contents(github_token, username, repo_name, item_path):
                    return False
            else:
                # Delete file
                delete_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{item_path}"
                delete_data = {
                    "message": f"Delete {item_path}",
                    "sha": item['sha'],
                    "branch": "main"
                }
                
                delete_response = requests.delete(delete_url, json=delete_data, headers=headers)
                delete_response.raise_for_status()
                logger.info(f"Deleted {item_path}")
            
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting repository contents: {str(e)}")
        return False

def create_github_repo(github_token: str, username: str, repo_name: str) -> bool:
    """Create GitHub repository if it doesn't exist"""
    try:
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Check if repo exists
        repo_url = f"https://api.github.com/repos/{username}/{repo_name}"
        response = requests.get(repo_url, headers=headers)
        
        if response.status_code == 404:
            # Create new repo
            create_url = "https://api.github.com/user/repos"
            repo_data = {
                "name": repo_name,
                "private": False,
                "auto_init": True
            }
            response = requests.post(create_url, json=repo_data, headers=headers)
            response.raise_for_status()
            logger.info(f"Created new repository: {repo_name}")
        else:
            logger.info(f"Repository {repo_name} already exists")
        
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating repository: {str(e)}")
        return False

def handle_file_upload(local_file_path: str, repo_path: str, github_token: str, username: str, repo_name: str) -> bool:
    """Upload a single file to the repository"""
    try:
        content_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{repo_path}"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Read and encode file content
        with open(local_file_path, "rb") as file:
            file_content = base64.b64encode(file.read()).decode("utf-8")
            
        file_data = {
            "message": f"Upload {repo_path}",
            "content": file_content,
            "branch": "main"
        }
        
        response = requests.put(content_url, json=file_data, headers=headers)
        response.raise_for_status()
        
        logger.info(f"✅ File '{repo_path}' uploaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"⚠️ Error uploading file {local_file_path}: {str(e)}")
        return False

def host_multi_files(dir_name: str, github_token: str, username: str, repo_name: str, current_path: str = "") -> bool:
    """
    Upload multiple files maintaining directory structure
    
    Args:
        dir_name: Root directory to upload
        github_token: GitHub personal access token
        username: GitHub username
        repo_name: Repository name
        current_path: Current path within the repository
    """
    try:
        # Initial setup - create repo and delete existing contents
        if not current_path:
            if not create_github_repo(github_token, username, repo_name):
                return False
            if not delete_repo_contents(github_token, username, repo_name):
                return False
            logger.info("Repository cleaned and ready for upload")
        
        # Check if directory exists
        if not os.path.exists(dir_name):
            logger.error(f"Directory {dir_name} does not exist")
            return False
            
        # Upload files
        for item in os.listdir(dir_name):
            full_path = os.path.join(dir_name, item)
            repo_path = os.path.join(current_path, item).replace("\\", "/")
            
            if os.path.isfile(full_path):
                if not handle_file_upload(full_path, repo_path, github_token, username, repo_name):
                    logger.error(f"Failed to upload {repo_path}")
            else:
                # Recursively handle subdirectories
                if not host_multi_files(full_path, github_token, username, repo_name, repo_path):
                    return False
                
        return True
        
    except Exception as e:
        logger.error(f"Error processing directory {dir_name}: {str(e)}")
        return False
def enable_github_pages():
    GITHUB_USERNAME = "psudeoR3BEL"
    GITHUB_TOKEN = "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"  # Replace with your actual token
    REPO_NAME = "complexProject2"
    GITHUB_API = "https://api.github.com"
    PAGES_API_URL = f"{GITHUB_API}/repos/{GITHUB_USERNAME}/{REPO_NAME}/pages"
    pages_data = {
        "source": {
            "branch": "main",
            "path": "/"
        }
    }
    response = requests.post(PAGES_API_URL, json=pages_data, auth=(GITHUB_USERNAME, GITHUB_TOKEN))
    if response.status_code in [201, 204,409]:
        print(f"✅ GitHub Pages enabled for {REPO_NAME}!")
        print(f"🔗 Your website will be available soon at: https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/")
        return f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/"
    else:
        print(f"⚠️ Error enabling GitHub Pages: {response.json()}")
        return False
def main(local_dir: str = "testProject"):
    # Configuration
    GITHUB_TOKEN = os.getenv("SECRET_KEY")
    GITHUB_USERNAME = "psudeoR3BEL"
    REPO_NAME = "complexProject2"
    
    success = host_multi_files(local_dir, GITHUB_TOKEN, GITHUB_USERNAME, REPO_NAME)
    
    if success:
        logger.info("✅ All files uploaded successfully!")
        return enable_github_pages()
    else:
        logger.error("⚠️ Some errors occurred during upload")
        return False