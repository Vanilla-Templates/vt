#!/usr/bin/env python3
"""
contains a logger function
"""
import sys
from colorama import init, Fore, Style


LogTypes = {
    0: f"{Fore.GREEN}[VT:INFO]{Style.RESET_ALL}",
    1: f"{Fore.YELLOW}[VT:WARNING]{Style.RESET_ALL}",
    2: f"{Fore.RED}[VT:ERROR]{Style.RESET_ALL}"
}

init(autoreset=True)  # Initialize colorama


def logger(message: str = "", log_type: int = 0):
    """
    prints message to stdout or stderr\n
    params:\n
    =======\n
    message: message to log
    log_type: file stream type
        0: ["INFO"] - stdout
        1: ["WARNING"] - stdout
        2: ["ERROR"] - stderr
    """
    if log_type not in range(3):
        raise ValueError("LogType doesn't exist (valid types are: 0 | 1 | 2)")

    log_prefix = LogTypes[log_type]
    log_message = f"\n{log_prefix}: {message}"

    if log_type in [0, 1]:
        print(log_message, file=sys.stdout)
    else:
        print(log_message, file=sys.stderr)

def print_error(message=""):
    """Only logs error/high-alert messages"""
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")


def print_success(message=""):
    """Only logs success messages"""
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")


def print_info(message=""):
    """Only logs info messages"""
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")