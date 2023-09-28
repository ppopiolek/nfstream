import scapy.all as scapy
import logging

def send_fake_handshake(src_ip, dst_ip, src_port, dst_port, interface="en1"):
    # Pakiet FIN
    fin = scapy.Ether() / scapy.IP(src=src_ip, dst=dst_ip) / scapy.TCP(sport=src_port, dport=dst_port, flags='F')
    scapy.sendp(fin, iface=interface)

    # Fałszywa odpowiedź FIN-ACK
    fin_ack = scapy.Ether() / scapy.IP(src=dst_ip, dst=src_ip) / scapy.TCP(sport=dst_port, dport=src_port, flags='FA')
    scapy.sendp(fin_ack, iface=interface)

    # Pakiet SYN
    syn = scapy.Ether() / scapy.IP(src=src_ip, dst=dst_ip) / scapy.TCP(sport=src_port, dport=dst_port, flags='S')
    scapy.sendp(syn, iface=interface)

    # Fałszywa odpowiedź SYN-ACK
    syn_ack = scapy.Ether() / scapy.IP(src=dst_ip, dst=src_ip) / scapy.TCP(sport=dst_port, dport=src_port, flags='SA')
    scapy.sendp(syn_ack, iface=interface)

    # Fałszywy pakiet ACK
    ack = scapy.Ether() / scapy.IP(src=src_ip, dst=dst_ip) / scapy.TCP(sport=src_port, dport=dst_port, flags='A')
    scapy.sendp(ack, iface=interface)

# Test the function
send_fake_handshake("66.220.156.68", "192.168.43.18", 443, 52066)
