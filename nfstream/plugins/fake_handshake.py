from nfstream import NFPlugin

import scapy.all as scapy
import logging
#podane musza byc parametry: handshake_type, interface


class FakeHandshake(NFPlugin):

    def on_init(self, packet, flow):
        pass

    def on_update(self, packet, flow):
        #if self.handshake_type == 1: - TODO: gdzies tu trzeba bedzie jeszcze uwzglednic typ tego handshake

        #fin expiration policy
        #if flow.bidirectional_fin_packets >= 2: #'==' a nie '>=' ze wzgledu na wyscigi itp
        #    flow.expiration_id = -1
        #    return

        def do_handshake():
        #TU BEDZIE OSTATECZNIE WYMYSLONY WARUNEK - LOGIKA ROZWIAZANIA
            return flow.bidirectional_packets >= 8 #na potrzeby testow niech bedzie 10
        
        
        def send_fake_handshake(src_ip, dst_ip, src_port, dst_port, interface):
            print("ROBIMY HANDSHAKE")
            print(flow.bidirectional_packets)
            # Pakiet FIN
            fin = scapy.Ether() / scapy.IP(src=src_ip, dst=dst_ip) / scapy.TCP(sport=src_port, dport=dst_port, flags='F')
            scapy.sendp(fin, iface=interface)

            # Fałszywa odpowiedź FIN-ACK
            fin_ack = scapy.Ether() / scapy.IP(src=dst_ip, dst=src_ip) / scapy.TCP(sport=dst_port, dport=src_port, flags='FA')
            scapy.sendp(fin_ack, iface=interface)

            #NA RAZIE POMIJAM ETAP NOWEGO HANDSHAKE I SKUPIAM SIE NA SAMYM FIN - ostatecznie mozna wykorzystac tcpreplay dla szybszego wysylania pakietów w bulk

            # Pakiet SYN
            #syn = scapy.Ether() / scapy.IP(src=src_ip, dst=dst_ip) / scapy.TCP(sport=src_port, dport=dst_port, flags='S')
            #scapy.sendp(syn, iface=interface)

            # Fałszywa odpowiedź SYN-ACK
            #syn_ack = scapy.Ether() / scapy.IP(src=dst_ip, dst=src_ip) / scapy.TCP(sport=dst_port, dport=src_port, flags='SA')
            #scapy.sendp(syn_ack, iface=interface)

            # Fałszywy pakiet ACK
            #ack = scapy.Ether() / scapy.IP(src=src_ip, dst=dst_ip) / scapy.TCP(sport=src_port, dport=dst_port, flags='A')
            #scapy.sendp(ack, iface=interface)


        if (do_handshake()):
            flow.expiration_id = -1 #expiration będzie ustawiany z automatu przy wysylaniu handshake a nie przy sniffowaniu aby uniknac bledow
            send_fake_handshake(flow.src_ip, flow.dst_ip, flow.src_port, flow.dst_port, self.interface)

    def on_expire(self, flow):
        print("expired")

