import argparse
import json
import os
from colorama import Fore, init
from packages.tool import Tool
from utils.show_tools import list_categories, print_tools

ITALIC = '\033[3m'
# Initialize colorama
init(autoreset=True)

BOLD = '\033[1m'
RESET = '\033[0m'
def load_manifest(manifest_path):
    """
    Load the manifest from a JSON file.
    """
    with open(manifest_path, 'r') as f:
        return json.load(f)

def run_specific_tool(manifest, folder, tool_name, args):
    """
    Run a specific tool given a folder and tool name.
    """
    if folder in manifest and tool_name in manifest[folder]:
        tool_info = manifest[folder][tool_name]
        tool = Tool(name=tool_info["name"],url=tool_info["url"], path=tool_info["path"], install_commands=tool_info["install"], run_command=tool_info["run"], description=tool_info["description"] if "description" in tool_info else None)
        tool.run(args)
    else:
        print(f"{Fore.RED}Tool '{tool_name}' not found in folder '{folder}' in the manifest.")
        
def man_specific_tool(manifest, folder, tool_name, args):
    """
    Man a specific tool given a folder and tool name.
    """
    if folder in manifest and tool_name in manifest[folder]:
        tool_info = manifest[folder][tool_name]
        tool = Tool(name=tool_info["name"],url=tool_info["url"] if "url" in tool_info else None, path=tool_info["path"], install_commands=tool_info["install"], run_command=tool_info["run"], description=tool_info["description"] if "description" in tool_info else None)
        tool.infos()
    else:
        print(f"{Fore.RED}Tool '{tool_name}' not found in folder '{folder}' in the manifest.")

def main():
    parser = argparse.ArgumentParser(description="Manage tools in the manifest.")
    parser.add_argument('-list_tools', action='store_true', help="List all tools")
    parser.add_argument('-list_categories', action='store_true', help="List all categories")
    parser.add_argument('command', nargs='?', help="Command to run")
    parser.add_argument('category', nargs='?', help="Category of the tool")
    parser.add_argument('tool_name', nargs='?', help="Tool name to run")
    parser.add_argument('args', nargs='*', help="Arguments for the tool")

    args = parser.parse_args()
    current_path = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(current_path, 'tools.json')
    manifest = load_manifest(manifest_path)

    if args.list_tools:
        print_tools(manifest)
        return
    
    

    if args.list_categories:
        list_categories(manifest)
        return
    
    if args.command == 'man' and args.category and args.tool_name:
        man_specific_tool(manifest, args.category, args.tool_name, args.args)
        return

    if args.command == 'run' and args.category and args.tool_name:
        run_specific_tool(manifest, args.category, args.tool_name, args.args)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
