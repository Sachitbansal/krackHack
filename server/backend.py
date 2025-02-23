import requests
from typing import Dict, Optional
import logging
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_api_request(url: str, user_input: str) -> dict:
    """Make an API request with error handling"""
    try:
        response = requests.post(
            url,
            json={"user_input": user_input},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise

def get_data_from_agent(prompt) -> Optional[Dict[str, Dict[str, str]]]:
    """Fetch data from agent and return file structure"""
    try:
        # API endpoints
        base_url = "https://api-lr.agent.ai/v1/agent/"
        design_endpoint = urljoin(base_url, "bzj3gxj532k08keq/webhook/b2c20880")
        code_endpoint = urljoin(base_url, "mfs3r5zucxquymkj/webhook/017c1ac3")
        file_endpoint = urljoin(base_url, "qv7ehw6pblvfpb20/webhook/3d4841e6")

        # Get initial design
        design_response = make_api_request(
            design_endpoint,
            prompt
        )
        
        data = design_response['response']
        
        # Get code for each part
        code_parts = [data['cssDesc'], data['htmlDesc'], data['jsDesc']]
        complete_code = ''
        for code_part in code_parts:
            code_response = make_api_request(code_endpoint, code_part)
            complete_code += code_response['response']
        
        # Get final file structure
        file_response = make_api_request(file_endpoint, complete_code)
        
        return file_response['response']
        
    except Exception as e:
        logger.error(f"Error in get_data_from_agent: {str(e)}")
        return None

if __name__ == "__main__":
    # Get the file data
    file_data = get_data_from_agent()
    
    if file_data:
        # Create the project structure
        from file_creator import create_project_structure
        success = create_project_structure(file_data)
        
        if success:
            print("Project created successfully!")
        else:
            print("Failed to create project")
    else:
        print("Failed to get data from agent")