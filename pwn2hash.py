#!/usr/bin/env python3
"""
Pwn2Hash - Handshake Extractor & Hashcat Cracker
Author: https://github.com/N4sh-x
License: MIT
Version: 1.2
GitHub: https://github.com/N4sh-x/Pwn2Hash

Description:
    This script automatically searches for WPA/WPA2 handshakes in .pcap/.cap files,
    converts them using hcxpcapngtool into a Hashcat-compatible format, and
    starts the cracking process using a specified wordlist.

Usage:
    python3 pwn2hash.py -t /path/to/handshakes -o /path/to/output -w /path/to/wordlist [options]

Options:
    -t, --target <dir>    : Directory containing .pcap/.cap files (default: /root/handshakes/)
    -o, --output <file>   : Output file for cracked passwords (default: cracked.txt)
    -w, --wordlist <file> : Wordlist for Hashcat (default: rockyou.txt)
    -m, --mode <int>      : Hashcat attack mode (default: 22000 for WPA/WPA2)
    -d, --device <int>    : GPU/CPU device for Hashcat (default: 0)
    -v, --verbose         : Enable verbose output
    -h, --help            : Show this help message and exit

Requirements:
    - hashcat
    - hcxpcapngtool (for conversion)
"""

import os
import argparse
import subprocess
import glob
import shutil
import sys

class MyParser(argparse.ArgumentParser):
    """ Custom error handling for argparse to show help on error """
    def error(self, message):
        sys.stderr.write(f"Error: {message}\n\n")
        self.print_help()
        sys.exit(2)
        
# ASCII Banner
def print_banner():
    banner = """
                     ________ .__                  .__     
________  _  ______  \_____  \|  |__ _____    _____|  |__  
\____ \ \/ \/ /    \  /  ____/|  |  \\__  \  /  ___/  |  \ 
|  |_> >     /   |  \/       \|   Y  \/ __ \_\___ \|   Y  \
|   __/ \/\_/|___|  /\_______ \___|  (____  /____  >___|  /
|__|              \/         \/    \/     \/     \/     \/ 

  Pwn2Hash - Handshake Extractor & Hashcat Cracker
    """
    print(banner)
    
def check_dependencies(verbose=False):
    """Checks if the required tools are installed."""
    required_tools = ["hcxpcapngtool", "hashcat"]
    for tool in required_tools:
        if not shutil.which(tool):
            print(f"[-] Error: {tool} not found. Install it and ensure it is in your PATH.")
            sys.exit(1)
        elif verbose:
            print(f"[+] {tool} found.")

def convert_handshakes(target_dir, output_file, verbose=False):
    """Converts all .pcap/.cap files into a single Hashcat-compatible file."""
    target_dir = os.path.abspath(target_dir)
    
    if not os.path.isdir(target_dir):
        print(f"[-] Error: Target directory {target_dir} does not exist.")
        sys.exit(1)

    handshake_files = glob.glob(os.path.join(target_dir, "*.cap")) + glob.glob(os.path.join(target_dir, "*.pcap"))
    if not handshake_files:
        print("[-] No handshake files found.")
        return None

    print(f"[+] Found {len(handshake_files)} handshake files.")
    
    base_name = os.path.splitext(output_file)[0]
    hash_file = base_name + "_22000.txt"
    
    command = ["hcxpcapngtool", "-o", hash_file, "-E", "exported.essid"] + handshake_files
    if verbose:
        print(f"[+] Executing conversion: {' '.join(command)}")
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0:
        print("[-] Conversion failed:")
        print(result.stderr)
        return None
    
    if verbose:
        print(f"[+] Conversion successful. Output file: {hash_file}")
    
    return hash_file

def run_hashcat(hash_file, wordlist, mode, output_file, device, verbose=False):
    """Starts Hashcat to crack the extracted handshakes."""
    if not os.path.exists(hash_file):
        print("[-] No valid hash file found. Exiting.")
        sys.exit(1)

    wordlist = os.path.abspath(wordlist)
    if not os.path.exists(wordlist):
        print(f"[-] Error: Wordlist file {wordlist} not found.")
        sys.exit(1)

    print(f"[+] Starting Hashcat (Mode {mode}, Device {device})...")

    command = [
        "hashcat", "-m", str(mode), hash_file, wordlist,
        "--force", "--optimized-kernel-enable", "--status", "--status-timer=10",
        "-o", output_file, "--device", str(device)
    ]
    
    if verbose:
        print(f"[+] Hashcat command: {' '.join(command)}")

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print("[-] Hashcat execution failed:")
        print(result.stderr)
        sys.exit(1)

    print(f"[+] Cracking complete. Results saved in {output_file}")

def main():
    """Main function for argument parsing and execution"""
    parser = MyParser(
        description="Pwn2Hash - Handshake Extractor & Hashcat Cracker",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-t", "--target", default="/root/handshakes/", help="Directory containing .pcap/.cap files (default: /root/handshakes/)")
    parser.add_argument("-o", "--output", default="cracked.txt", help="Output file for cracked passwords (default: cracked.txt)")
    parser.add_argument("-w", "--wordlist", default="rockyou.txt", help="Wordlist for Hashcat (default: rockyou.txt)")
    parser.add_argument("-m", "--mode", type=int, default=22000, help="Hashcat attack mode (default: 22000 for WPA/WPA2)")
    parser.add_argument("-d", "--device", type=int, default=0, help="Hashcat device (default: 0)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

     print_banner()

    # Check dependencies before proceeding
    check_dependencies(args.verbose)

    # Convert handshake files
    hash_file = convert_handshakes(args.target, args.output, args.verbose)

    if hash_file:
        # Run Hashcat if handshake file was successfully created
        run_hashcat(hash_file, args.wordlist, args.mode, args.output, args.device, args.verbose)

if __name__ == "__main__":
    main()
