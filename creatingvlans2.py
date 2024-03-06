import socket
import time

# Router credentials
router_ip = "192.168.21.134"  # Replace with your router's IP
username = "admin"
password = "bilal"  # Replace with your router's password

# Commands to create VLAN and assign to interface
vlan_id = 100  # Replace with your desired VLAN ID
commands = [
    f"/interface vlan add interface=ether3-lan name=vlan{vlan_id} vlan-id={vlan_id}",
    f"/interface bridge add name=bridge{vlan_id}",
    f"/interface bridge port add bridge=bridge{vlan_id} interface=vlan{vlan_id}",
]

# Connect to the router via Telnet
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"Connecting to {router_ip} on port 23...")
    s.connect((router_ip, 23))  # Telnet port 23

    # Wait for login prompt
    data = s.recv(1024).decode()
    if b"Login:" in data:
        print("Sending username...")
        s.sendall((username + "\n").encode())
        data = s.recv(1024).decode()
        print(f"Received: {data.strip()}")

    # Wait for password prompt
    if b"Password:" in data:
        print("Sending password...")
        s.sendall((password + "\n").encode())
        data = s.recv(1024).decode()
        print(f"Received: {data.strip()}")  # Password prompt responses are typically hidden

    # Send commands one by one, waiting for a prompt after each
    for command in commands:
        print(f"Sending command: {command}")
        s.sendall((command + "\n").encode())
        time.sleep(1)  # Allow time for command execution
        data = s.recv(1024).decode()
        print(f"Received: {data.strip()}")

print("VLAN configuration completed.")