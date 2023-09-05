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
            "bidirectional_packets": flow.bidirectional_packets,
            "time": time.time()  # Dodatkowy przykład, jak zapisać aktualny czas.
        })
        #print(f"[DEBUG] Updated flow: {flow_hash}")  # Debugowanie aktualizacji.

    def on_expire(self, flow):
        print('flow--')
        flow_hash = flow.__hash__()
        self.live_data.remove(flow_hash)
        print(f"[DEBUG] Flow expired: {flow_hash}")  # Dodatkowy komunikat debugowy

