import sys
import socket
import struct

# Function to create a VLAN
def create_vlan(router_ip, username, password, vlan_id, interface):
  # Connect to the router
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.21.134', 8728))  # Connect to the API port
    print(f"Connected to router at {router_ip}:{8728}")
  except socket.error as e:
    print("Error connecting to the router:", e)
    sys.exit(1)

  # Login to the router
  try:
    print("Sending login command...")
    s.send(b'/login\n')
    print(f"Sending login credentials: username={username}, password={password}")
    s.send(f'/login username={username} password={password}\n'.encode())
    response = s.recv(4096).decode()
    print(f"Received response: {response}")
    if "!done" not in response:
      print("Login failed. Exiting.")
      sys.exit(1)
  except socket.error as e:
    print("Error logging in:", e)
    sys.exit(1)

  # Create the VLAN
  try:
    print("Sending VLAN creation command...")
    command = f'/interface vlan add name=vlan{vlan_id} interface={interface} vlan-id={vlan_id}\n'.encode()
    s.send(command)
    print(f"Sent command: {command.decode()}")
    response = s.recv(4096).decode()
    print(f"Received response: {response}")
    if "!done" in response:
      print(f"VLAN {vlan_id} created successfully.")
    else:
      print("Failed to create VLAN.")
  except socket.error as e:
    print("Error creating VLAN:", e)
    sys.exit(1)

  # Close the connection
  s.close()

# Usage example
if __name__ == "__main__":
  router_ip = "192.168.21.134"
  username = "admin"
  password = "bilal"
  vlan_id = 300
  interface = "ether3-lan"  # Specify the interface to assign the VLAN to

  create_vlan(router_ip, username, password, vlan_id, interface)
