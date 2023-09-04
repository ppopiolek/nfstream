from nfstream import NFStreamer, verify_version, plugins

if __name__ == '__main__':
    print(verify_version())
    print("Running listener on en0...")
    streamer = NFStreamer(source="en0", udps = [plugins.LIVE_PARAMETERS()], statistical_analysis= True) 
    for flow in streamer:
        print(f"Flow ended: {flow.id}")
