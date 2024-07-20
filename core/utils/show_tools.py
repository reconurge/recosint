
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)
BOLD = '\033[1m'
RESET = '\033[0m'
def print_tools(tree, parent=""):
    """
    Recursively prints tools with their appropriate parents.
    """
    for key, value in tree.items():
        if isinstance(value, dict):
            # Check if it is a tool with 'install' or 'run' key
            if 'install' in value or 'run' in value:
                # Tool is active
                if parent != "":
                    print(f"{BOLD}{Fore.GREEN}{parent + '/' if parent else ''}{key}{RESET}")   
            else:
                # Tool is disabled
                if parent != "":
                    print(f"{Fore.LIGHTBLACK_EX}{parent + '/' if parent else ''}{key}")
            # Recursively print sub-tools or categories
            print_tools(value, parent + '/' + key if parent else key)
        else:
            # If it's not a dict, ignore (shouldn't happen in a correct manifest)
            continue

def list_categories(manifest):
    """
    List categories (parent folders) and the number of tools in each.
    """
    print("Categories and tool counts:")
    for category, tools in manifest.items():
        print(f"{BOLD}{Fore.GREEN}{category}: {len(tools)} tool(s)")