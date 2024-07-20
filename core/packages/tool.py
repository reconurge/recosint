import os
import subprocess
import sys

from colorama import Fore
from pathlib import Path

class Tool:
    def __init__(self, name, path, install_commands, run_command):
        self.name = name
        self.path = str(Path(__file__).parent.parent) + path
        self.install_commands = install_commands
        self.run_command =run_command

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
