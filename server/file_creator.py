import os
import json
from typing import Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        # Create main project directory
        if not os.path.exists(project_name):
            os.makedirs(project_name)
            logger.info(f"Created project directory: {project_name}")
        
        # Create and write files
        for file_type, files in file_data.items():
            for file_name, content in files.items():
                file_path = os.path.join(project_name, file_name)
                
                # Write file content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                logger.info(f"Created file: {file_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error creating project structure: {str(e)}")
        return False

def main():
    # Sample file data (you can replace this with your actual data)
    file_data = {
        'css': {
            'style.css': """body {
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 0;
    background-color: #fff8e1;
}
/* ... rest of CSS ... */"""
        },
        'html': {
            'index.html': """<!DOCTYPE html>
<html lang="en">
<!-- ... rest of HTML ... -->
</html>"""
        },
        'js': {
            'script.js': """document.addEventListener('DOMContentLoaded', function() {
    // ... rest of JavaScript ...
});"""
        }
    }
    
    # Create the project structure
    success = create_project_structure(file_data)
    
    if success:
        logger.info("Project structure created successfully!")
    else:
        logger.error("Failed to create project structure")

if __name__ == "__main__":
    main()