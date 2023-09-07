import socket
import time

# Define the IP address and port of the server to connect to
HOST = '172.17.0.2'
PORT = 65432

# Create a socket using IPv4 and TCP protocol
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    # Connect to the server using the specified IP and port
    s.connect((HOST, PORT))
    
    # Define the time to keep the communication active (e.g., 60 seconds)
    end_time = time.time() + 60  
    
    # Keep communicating until the end_time is reached
    while time.time() < end_time:
        
        # Send a message to the server
        s.sendall(b'Client message')
        
        # Receive a response from the server
        data = s.recv(1024)
        
        # Wait for a second before sending the next message
        time.sleep(1)  
    
    # Shutdown the connection and send TCP FIN flag to the server
    s.shutdown(socket.SHUT_RDWR)
    s.close()
