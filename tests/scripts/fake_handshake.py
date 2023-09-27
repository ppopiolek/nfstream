import socket
import struct
import os

def send_fake_handshake(src_ip, dst_ip, src_port, dst_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # Wypełnienie pakietu losowymi bajtami
    data = os.urandom(40)  # 40 losowych bajtów

    # Nagłówek TCP dla pakietu SYN
    tcp_header = struct.pack('!HHLLBBHHH', src_port, dst_port, 0, 0, 80, 2, 5840, 0, 0) + data

    # Nagłówek IP z poprawioną długością całkowitą
    total_length = 20 + len(tcp_header)
    ip_header = struct.pack('!BBHHHBBH4s4s', 69, 0, total_length, 54321, 0, 64, socket.IPPROTO_TCP, 0, socket.inet_aton(src_ip), socket.inet_aton(dst_ip))
    
    s.sendto(ip_header + tcp_header, (dst_ip, 0))

    # Nagłówek TCP dla fałszywej odpowiedzi SYN-ACK
    tcp_header_syn_ack = struct.pack('!HHLLBBHHH', dst_port, src_port, 0, 1, 80, 18, 5840, 0, 0) + data
    s.sendto(ip_header + tcp_header_syn_ack, (src_ip, 0))

    # Nagłówek TCP dla fałszywego pakietu ACK
    tcp_header_ack = struct.pack('!HHLLBBHHH', src_port, dst_port, 1, 1, 80, 16, 5840, 0, 0) + data
    s.sendto(ip_header + tcp_header_ack, (dst_ip, 0))
    
    s.close()

# Test the function
send_fake_handshake("192.168.1.1", "192.168.1.2", 12345, 80)
