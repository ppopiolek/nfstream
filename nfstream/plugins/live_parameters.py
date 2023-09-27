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
        print('flow--')
        flow_hash = flow.__hash__()
        self.live_data.remove(flow_hash)
        print(f"[DEBUG] Flow expired: {flow_hash}")  # Dodatkowy komunikat debugowy

