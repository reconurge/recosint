import os
import subprocess
import sys
from pathlib import Path
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

BOLD = '\033[1m'
RESET = '\033[0m'
ITALIC = '\033[3m'

class Tool:
    def __init__(self, name,url,  path, install_commands, run_command, description):
        self.name = name
        self.url=url
        self.path = str(Path(__file__).parent.parent) + path
        self.install_commands = install_commands
        self.run_command = run_command
        self.description = description

    def install_tool(self):
        """
        Install the tool by executing the install commands.
        """
        print(f"Changing directory to {self.path}")
        # Ensure the base path exists
        os.makedirs(self.path, exist_ok=True)
        os.chdir(self.path)


        # Execute each install command
        for command in self.install_commands:
            print(f"Running install command: {command}")
            try:
                subprocess.check_call(command, shell=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to execute: {command}. Error: {e}")
                sys.exit(1)

    def is_tool_installed(self):
        """
        Checks if a folder is empty.
        """
        if os.path.exists(self.path):
            return not any(self.path)
        return True

    def run(self, args):
        """
        Run the tool with the given arguments.
        """
        if not self.install_commands or not self.run_command:
            print(f"{Fore.RED}Tool {self.name} doesn't provide an install setup. Skipping...")
            return

        if self.is_tool_installed():
            print(f"{Fore.LIGHTBLACK_EX}Tool {self.path} not yet installed. Installing..")
            self.install_tool()
        else:
            print(f"{Fore.LIGHTBLACK_EX}Tool {self.path} already installed. Skipping installation.")
        run_command = f'{self.run_command} {" ".join(args)}'

        # Change to the tool's directory
        os.chdir(self.path)
        
        # Execute the run command
        print(f"Running command: {run_command}")
        try:
            subprocess.check_call(run_command, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute: {run_command}. Error: {e}")
            sys.exit(1)

    def infos(self):
        """
        Prints infos about a particular tool.
        """
        print(f"\n{BOLD}{Fore.CYAN}{self.name}")
        print(f"{Fore.CYAN}{self.url}")
        if self.description:
            print(f"\n{Fore.YELLOW}{self.description}")
        else:
            print(f"\n{Fore.YELLOW}{ITALIC}No description provided.") 
            
        print(f"\nInstall commands:")
        print("\n".join(f"{Fore.LIGHTCYAN_EX} -  {command}" for command in list(self.install_commands)))
        
        print(f"\n{Fore.LIGHTYELLOW_EX}Tool located in {ITALIC}{self.path}.\n") 

