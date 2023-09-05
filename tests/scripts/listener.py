from nfstream import NFStreamer, verify_version, plugins
import multiprocessing
import time

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
    streamer = NFStreamer(source="en0", udps=[plugins.LIVE_PARAMETERS(live_data=live_data)], statistical_analysis=True)
    for flow in streamer:
        pass
    print("[INFO] NFStreamer has finished processing.")

if __name__ == '__main__':
    live_data = LiveData()
    print("[INFO] Starting streamer process...")
    streamer_process = multiprocessing.Process(target=streamer_function, args=(live_data,))
    streamer_process.start()

    print("[INFO] Entering main loop...")
    while True:
        time.sleep(10)
        print("[INFO] Fetching current live flows...")
        current_flows = live_data.get_all()
        print(f"[DEBUG] Total number of live flows: {len(current_flows)}")
        
        for flow_hash, flow_data in current_flows.items():
            print(f"Flow Hash: {flow_hash}")
            print(f"Bi-directional Packets: {flow_data['bidirectional_packets']}")
            print("-------------------------------")
