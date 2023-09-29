from nfstream import NFStreamer, plugins

INTERFACE = 'en1'

streamer = NFStreamer(source=INTERFACE, udps=[plugins.FakeHandshake(interface = INTERFACE)], statistical_analysis=True)
for flow in streamer:
    #print(flow)
    pass