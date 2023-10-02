from nfstream import NFPlugin

import scapy.all as scapy
import logging
#podane musza byc parametry: handshake_type, interface


class FakeHandshake(NFPlugin):

    def on_init(self, packet, flow):
        pass

    def on_update(self, packet, flow):
        #if self.handshake_type == 1: - TODO: gdzies tu trzeba bedzie jeszcze uwzglednic typ tego handshake

        #Dla pliku NormalCaptures/2017-04-28_normal.pcap:
        #Mean duration: 13567.875947347427
        #Mean packets: 13.213668395160218
        #Mean bytes: 7660.834662943757
        DURATION = 13567.875947347427
        PACKETS = 13.213668395160218
        BYTES = 7660.834662943757

        if (flow.bidirectional_fin_packets >= 2):
            flow.expiration_id = -1


        def do_handshake():

            packets = flow.bidirectional_packets >= PACKETS - 3 # zaokr. w dol
            bytes = flow.bidirectional_bytes >= BYTES - 109 # zaokr. w dol
            duration = flow.bidirectional_duration_ms >= DURATION - 1

            return (((packets + bytes + duration) >= 1) & (flow.vlan_id != 777)) # 777 means flow "logically" expired
        
        
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
            syn = scapy.Ether() / scapy.IP(src=src_ip, dst=dst_ip) / scapy.TCP(sport=src_port, dport=dst_port, flags='S')
            scapy.sendp(syn, iface=interface)

            # Fałszywa odpowiedź SYN-ACK
            syn_ack = scapy.Ether() / scapy.IP(src=dst_ip, dst=src_ip) / scapy.TCP(sport=dst_port, dport=src_port, flags='SA')
            scapy.sendp(syn_ack, iface=interface)

            # Fałszywy pakiet ACK
            ack = scapy.Ether() / scapy.IP(src=src_ip, dst=dst_ip) / scapy.TCP(sport=src_port, dport=dst_port, flags='A')
            scapy.sendp(ack, iface=interface)


        if (do_handshake()):
            # TU MUSI BYC JAKIES INFO ZE JEST EXPIRED ZEBY NIE POWTARZAC
            flow.vlan_id = 777 #expiration będzie ustawiany z automatu przy wysylaniu handshake a nie przy sniffowaniu aby uniknac bledow
            
            # policzenie kto bedzie src a kto dst dla fake handshake (jako ze handshake ma najwiekszy stosunkowy wplyw na ilosc pakietow to to bedzie parametr po ktoym bedzie decyzja)
            if (flow.src2dst_packets > flow.dst2src_packets):
                send_fake_handshake(flow.dst_ip, flow.src_ip, flow.dst_port, flow.src_port, self.interface)
            else:
                send_fake_handshake(flow.src_ip, flow.dst_ip, flow.src_port, flow.dst_port, self.interface)

    def on_expire(self, flow):
        print("expired")

