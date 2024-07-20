import os
import subprocess
import sys

from colorama import Fore

def install_tool(tool_info):
    """
    Install the tool by executing the install commands.
    """
    path = tool_info["path"]
    install_commands = tool_info["install"]
    print(f"Changing directory to {path}")
    os.chdir(path)

    
    # Ensure the base path exists
    os.makedirs(path, exist_ok=True)

    # Execute each install command
    for command in install_commands:
        print(f"Running install command: {command}")
        try:
            subprocess.check_call(command, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute: {command}. Error: {e}")
            sys.exit(1)

def is_folder_empty(folder_path):
    """
    Checks if a folder is empty.
    """
    if os.path.exists(folder_path):
        return not any(os.scandir(folder_path))
    return True

def run_tool(tool_info, args):
    """
    Run the tool with the given arguments.
    """
    if "install" not in tool_info:
        print(f"{Fore.RED}Tool {tool_info['name']} doesn't provide an install setup. Skipping...")
        return

    path = tool_info["path"]
    if is_folder_empty(path):
        print(f"{Fore.LIGHTBLACK_EX}Tool {path} not yet installed. Installing..")
        install_tool(tool_info)
    else:
        print(f"{Fore.LIGHTBLACK_EX}Tool {path} already installed. Skipping installation.")
    path = tool_info["path"]
    run_command = f'{tool_info["run"]} {" ".join(args)}'

    # Change to the tool's directory
    os.chdir(path)
    
    # Execute the run command
    print(f"Running command: {run_command}")
    try:
        subprocess.check_call(run_command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute: {run_command}. Error: {e}")
        sys.exit(1)