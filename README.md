# Pwn2Hash

Pwn2Hash is an automated tool for extracting WPA/WPA2 handshakes from .pcap/.cap files, converting them into a Hashcat-compatible format, and launching a dictionary attack to crack Wi-Fi passwords.

## Features
- Automatic detection of WPA/WPA2 handshakes
- Converts .pcap/.cap files to Hashcat format using `hcxpcapngtool`
- Supports GPU and CPU cracking with `hashcat`
- Customizable Hashcat attack modes and device selection
- Verbose mode for detailed process tracking

## Requirements
- Python 3.x
- Tools: `hashcat`, `hcxpcapngtool`

## Installation
Clone the repository:
```bash
git clone https://github.com/N4sh-x/Pwn2Hash.git
```
Ensure all required tools are installed and available in your system's PATH:
```bash
sudo apt install hashcat hcxpcapngtool -y
```

## Usage
Run the script with:
```bash
python3 pwn2hash.py -t <target_directory> -o <output_file> -w <wordlist> [options]
```

## Options
| Option | Description |
|--------|-------------|
| `-t, --target` | Directory containing .pcap/.cap files (default: `/root/handshakes/`) |
| `-o, --output` | Output file for cracked passwords (default: `cracked.txt`) |
| `-w, --wordlist` | Wordlist for Hashcat (default: `rockyou.txt`) |
| `-m, --mode` | Hashcat attack mode (default: `22000` for WPA/WPA2) |
| `-d, --device` | GPU/CPU device for Hashcat (default: `0`) |
| `-v, --verbose` | Enable verbose output |
| `-h, --help` | Show help message and exit |

## Example
```bash
python3 pwn2hash.py -t /home/user/captures -o results.txt -w /usr/share/wordlists/rockyou.txt -m 22000 -d 1 -v
```

## License
This project is licensed under the MIT License.

## ⚠ Disclaimer
This tool is intended only for legal security assessments and authorized penetration testing. Unauthorized use is strictly prohibited and may violate laws.
