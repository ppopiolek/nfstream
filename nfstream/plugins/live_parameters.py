from nfstream import NFPlugin
import time

class LIVE_PARAMETERS(NFPlugin):
    def __init__(self, live_data):
        super().__init__()
        self.live_data = live_data

    def on_init(self, packet, flow):
        #print('flow++')
        #print(flow.__hash__())
        pass

    def on_update(self, packet, flow):
        flow_hash = flow.__hash__()
        self.live_data.update(flow_hash, {
            #DURATION
            "bidirectional_duration_ms": flow.bidirectional_duration_ms,
            #PACKETS
            "bidirectional_packets": flow.bidirectional_packets,
            #PACKET SIZEŚ
            "bidirectional_bytes": flow.bidirectional_bytes,

            #POTRZEBNE DO FAKE HANDSHAKE
            "src_ip": flow.src_ip,
            "dst_ip": flow.dst_ip,
            "src_port": flow.src_port,
            "dst_port": flow.dst_port,
            "bidirectional_fin_packets": flow.bidirectional_fin_packets,
            

            #ew. pozostałe parametry potrzebne do opracowanych heurystyk

            #flags total(?)

            #TODO: statistical params
            #packet size (stst)
            #piat (stat)
            #header size (stat)

        })

        
        #SPRAWDZENIE ILE RAZY BEDA DWA PAKIETY WE FLOW - TO WSZYSTKO SLUZY TYLKO DO TESTOWANIA PROJEKTOWANEGO ROZWIAZANIA
        if flow.bidirectional_packets == 2:
                print(flow_hash)

    def on_expire(self, flow):
        flow_hash = flow.__hash__()
        self.live_data.remove(flow_hash)
        #print(f"[DEBUG] Flow expired: {flow_hash}")  # Dodatkowy komunikat debugowy

