from nfstream import NFStreamer, verify_version, plugins
import multiprocessing
import time

INTERFACE = 'en1'

class LiveData:
    def __init__(self):
        manager = multiprocessing.Manager()
        self.data = manager.dict()  # Używamy słownika zarządzanego przez Manager
        self.lock = manager.Lock()  # Blokada zarządzana przez Manager

    def update(self, flow_hash, value):
        with self.lock:
            self.data[flow_hash] = value

    def remove(self, flow_hash):
        with self.lock:
            if flow_hash in self.data:
                del self.data[flow_hash]

    def get_all(self):
        with self.lock:
            return dict(self.data)  # Konwertujemy na standardowy słownik

def streamer_function(live_data):
    print("[INFO] Starting NFStreamer...")
    streamer = NFStreamer(source=INTERFACE, udps=[plugins.LIVE_PARAMETERS(live_data=live_data), plugins.FlowSlicer(fin_limit=2)], statistical_analysis=True)
    for flow in streamer:
        pass
    print("[INFO] NFStreamer has finished processing.")

import scapy.all as scapy
import logging

def send_fake_handshake(src_ip, dst_ip, src_port, dst_port, interface=INTERFACE):
    print("ROBIMY HANDSHAKE")
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
    scapy.sendp(ack, iface=INTERFACE)


if __name__ == '__main__':
    live_data = LiveData()
    print("[INFO] Starting streamer process...")
    streamer_process = multiprocessing.Process(target=streamer_function, args=(live_data,))
    streamer_process.start()

    print("[INFO] Entering main loop...")
    while True:
        #time.sleep(10) - to by zostało jeśli sprawdzenie miałoby się odbywać co jakiś czas
        #print("[INFO] Fetching current live flows...")
        current_flows = live_data.get_all()
        #print(f"[DEBUG] Total number of live flows: {len(current_flows)}")

        for flow_hash, flow_data in current_flows.items():
            making_handshake = False
            def do_handshake():
                return ((flow_data['bidirectional_packets']>= 10) & (making_handshake == False))
            if (do_handshake()):
                X = flow_data['bidirectional_packets']
                print(f'BIDIRECRTIONAL {X}')
                #simulate_handshake(flow_data['src_ip'], flow_data['dst_ip'], flow_data['src_port'], flow_data['dst_port'], flow_data['protocol'], flow_data['vlan_id'], flow_data['tunnel_id'])
                making_handshake = True
                send_fake_handshake(flow_data['src_ip'], flow_data['dst_ip'], flow_data['src_port'], flow_data['dst_port'])
                making_handshake = False

            #print(f"Flow Hash: {flow_hash}")
            #print(f"Bi-directional Packets: {flow_data['bidirectional_packets']}")
            #print("-------------------------------")