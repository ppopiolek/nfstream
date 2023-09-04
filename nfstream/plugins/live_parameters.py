from nfstream import NFPlugin


class LIVE_PARAMETERS(NFPlugin):

    def on_init(self, packet, flow): #ON INIT MOGE DAC JAKIES OZNACZENIE ZE TO BEDZIE KOMUNIKACJA ZLOSLIWA
        """
        on_init(self, obs, flow): Method called at flow creation.
        You must initiate your udps values if you plan to compute ones.
        Example: -------------------------------------------------------
                 flow.udps.magic_message = "NO"
                 if packet.raw_size == 40:
                    flow.udps.packet_40_count = 1
                 else:
                    flow.udps.packet_40_count = 0
        ----------------------------------------------------------------
        """

    def on_update(self, packet, flow): #ON UPDATE WSZELKIE PARAMETRY KTORYCH NIE MA ZAIMPLEMENTOWANYCH
        """
        on_update(self, obs, flow): Method called to update each flow with its belonging packet.
        Example: -------------------------------------------------------
                 if packet.raw_size == 40:
                    flow.udps.packet_40_count += 1
        ----------------------------------------------------------------
        """
        print(f"Protocol: {flow.protocol}, IP Src: {flow.src_ip}, IP Dst: {flow.dst_ip}, Port Src: {flow.src_port}, Port Dst: {flow.dst_port}")
        print("Total packets:", flow.bidirectional_packets)
        print("Total bytes:", flow.bidirectional_bytes)

        try:
            print(f'Bidirectional_mean_piat: {flow.bidirectional_mean_piat_ms}')
        except:
            print('Statistical analysis error')



    def on_expire(self, flow):
        """
        on_expire(self, flow):      Method called at flow expiration.
        Example: -------------------------------------------------------
                 if flow.udps.packet_40_count >= 10:
                    flow.udps.magic_message = "YES"
        ----------------------------------------------------------------
        """

    def cleanup(self):
        """
        cleanup(self):               Method called for plugin cleanup.
        Example: -------------------------------------------------------
                 del self.large_dict_passed_as_plugin_attribute
        ----------------------------------------------------------------
        """
