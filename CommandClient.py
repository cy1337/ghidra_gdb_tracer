#!/usr/bin/env python3

import socket
import sys

def send_command(opcode, input_file, ip, port):
    # Read data from the input file
    with open(input_file, 'r') as file:
        data = file.read()

    # Prepare the command with opcode and length encoding
    data_length = len(data).to_bytes(2, byteorder='big')  # Assuming 2 bytes for length
    opcode = int(opcode).to_bytes(1, byteorder='big')  # Assuming 1 byte for opcode
    command = opcode + data_length + data.encode()

    # Send the command to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(command)
        response = s.recv(1024)
    return response

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python send_command.py <opcode> <input_file> <ip:port>")
        sys.exit(1)

    opcode = sys.argv[1]
    input_file = sys.argv[2]
    ip_port = sys.argv[3].split(':')
    ip = ip_port[0]
    port = int(ip_port[1]) if len(ip_port) > 1 else 8080  # Default port 8080

    response = send_command(opcode, input_file, ip, port)
    print("Received response:", response.decode())
