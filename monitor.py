from scapy.all import sniff
from collections import defaultdict
from rich.console import Console
from rich.table import Table
import threading
import time
import argparse

parser = argparse.ArgumentParser(description="Monitor network ports and source IPs.")
parser.add_argument("--full-ips", action="store_true", help="Display full IP addresses without truncation")
parser.add_argument("--refresh", type=int, default=3, help="Refresh interval in seconds (default: 3)")
args = parser.parse_args()

port_connections = defaultdict(lambda: defaultdict(set))
console = Console()

def packet_callback(packet):
    if packet.haslayer("IP") and packet.haslayer("TCP"):
        src_ip = packet["IP"].src
        dst_ip = packet["IP"].dst
        dst_port = packet["TCP"].dport
        port_connections[dst_port][dst_ip].add(src_ip)
    elif packet.haslayer("IP") and packet.haslayer("UDP"):
        src_ip = packet["IP"].src
        dst_ip = packet["IP"].dst
        dst_port = packet["UDP"].dport
        port_connections[dst_port][dst_ip].add(src_ip)

def capture_packets():
    sniff(prn=packet_callback, store=False)

def display_tables():
    while True:
        console.clear()
        valid_ports = {}
        total_connections = 0
        
        for port, dst_ips in port_connections.items():
            for dst_ip, src_ips in dst_ips.items():
                if len(src_ips) >= 2:
                    valid_ports[f"{port} ({dst_ip}) ({len(src_ips)})"] = src_ips
                    total_connections += len(src_ips)
        
        if valid_ports:
            table_ports = Table(title="Used Ports and Source IPs")
            
            for col_name in sorted(valid_ports.keys()):
                table_ports.add_column(col_name, justify="center", style="cyan", overflow="fold" if args.full_ips else "ellipsis")
            
            max_ips = max(len(ips) for ips in valid_ports.values())
            rows = [[] for _ in range(max_ips)]
            
            for col_name in sorted(valid_ports.keys()):
                ip_list = list(sorted(valid_ports[col_name]))
                for i in range(max_ips):
                    if i < len(ip_list):
                        rows[i].append(ip_list[i])
                    else:
                        rows[i].append("")
            
            for row in rows:
                table_ports.add_row(*row)
            
            console.print(table_ports)
        
        table_total = Table(title="Connection Statistics")
        table_total.add_column("Total Connections", justify="center", style="bold red")
        table_total.add_row(str(total_connections))
        console.print(table_total)
        
        time.sleep(args.refresh)

if __name__ == "__main__":
    thread_sniff = threading.Thread(target=capture_packets, daemon=True)
    thread_sniff.start()
    display_tables()