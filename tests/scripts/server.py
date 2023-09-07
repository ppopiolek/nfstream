import socket
import time

# Define the IP address and port for the server to listen on
HOST = '0.0.0.0'
PORT = 65432

# Create a socket using IPv4 and TCP protocol
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    # Bind the socket to the specified IP and port
    s.bind((HOST, PORT))
    
    # Start listening for incoming connections
    s.listen()
    
    # Accept a connection from a client
    conn, addr = s.accept()
    
    with conn:
        print('Connected by', addr)
        
        # Define the time to keep the communication active (e.g., 60 seconds)
        end_time = time.time() + 60  
        
        # Keep communicating until the end_time is reached
        while time.time() < end_time:
            
            # Receive data from the client
            data = conn.recv(1024)
            
            # If no data is received, break out of the loop
            if not data:
                break
            
            # Send a response back to the client
            conn.sendall(b'Server response')
        
        # Shutdown the connection and send TCP FIN flag to the client
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
