from nfstream import NFPlugin
import time

class LIVE_PARAMETERS(NFPlugin):
    def __init__(self, live_data):
        super().__init__()
        self.live_data = live_data

    def on_init(self, packet, flow):
        print('flow++')
        pass

    def on_update(self, packet, flow):
        flow_hash = flow.__hash__()
        self.live_data.update(flow_hash, {
            #duration total
            "bidirectional_duration_ms": flow.bidirectional_duration_ms,
            #packets total
            "bidirectional_packets": flow.bidirectional_packets,
            #bytes (ps) total
            #header size total
            #flags total
            #packet size (stst)
            #piat (stat)
            #header size (stat)

        })
        #print(f"[DEBUG] Updated flow: {flow_hash}")  # Debugowanie aktualizacji.

    def on_expire(self, flow):
        print('flow--')
        flow_hash = flow.__hash__()
        self.live_data.remove(flow_hash)
        print(f"[DEBUG] Flow expired: {flow_hash}")  # Dodatkowy komunikat debugowy

