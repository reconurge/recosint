import os
import json

def read_git_link(filepath):
    """
    Reads the git repository link from a .git file.
    """
    try:
        with open(filepath, 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def generate_json_tree(root_dir):
    """
    Recursively generates a JSON tree from the directory structure.
    """
    tree = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Create a nested dictionary for each directory
        folder = os.path.relpath(dirpath, root_dir)
        parts = folder.split(os.sep)
        current_level = tree

        for part in parts:
            if part not in current_level:
                obj = {} if dirnames else {"name": part, "path": dirpath}
                current_level[part] = obj
            current_level = current_level[part]

        for filename in filenames:
            if filename == '.git':
                tool_name = os.path.basename(dirpath)
                git_link = read_git_link(os.path.join(dirpath, filename))
                if git_link:
                    current_level[tool_name] = {
                        "install": f"git clone {git_link} {tool_name}",
                        "run": f"./{tool_name}"
                    }
    
    return tree

def save_json_tree(tree, output_file):
    """
    Saves the JSON tree to a file.
    """
    with open(output_file, 'w') as f:
        json.dump(tree, f, indent=4)
