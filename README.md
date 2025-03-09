# Live Port Monitor

## Overview
**Live Port Monitor** is a Python script that monitors and displays active network ports in real-time. It captures incoming network traffic, identifying source IPs communicating with specific destination ports, and presents the data in a structured, dynamically updating table.

The script leverages `scapy` for packet sniffing and `rich` for an interactive, visually enhanced console output.

## Features
- **Real-time monitoring** of TCP and UDP traffic.
- **Dynamic table display** using `rich`, showing active ports and associated source IPs.
- **Filter active ports** by displaying only those with at least two unique source IPs.
- **Auto-refreshing output** (default: every 3 seconds).
- **Customizable refresh interval** using `--refresh` argument.
- **Option to display full source IPs** with `--full-ips` argument.
- **Summary tables** showing total active connections and the number of unique ports in use.

## Installation
Ensure you have Python installed, then install the required dependencies:

```bash
pip install scapy rich
```
