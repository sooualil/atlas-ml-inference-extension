from scapy.all import IP, TCP, DNS, DNSRR

class AuxTCPWindowMinMAx(NFPlugin):
    def __init__(self):
        super(AuxTCPWindowMinMAx, self).__init__()

    def on_init(self, packet, flow):
        
        flow.udps.tcp_win_max_in = 0
        flow.udps.tcp_win_max_out = 0
        try:
            s_packet = IP(packet.ip_packet)
            if s_packet.haslayer(TCP):
                flow.udps.tcp_win_max_in = s_packet[TCP].window
                flow.udps.tcp_win_max_out = s_packet[TCP].window
                
        except :
            return
        

    def on_update(self, packet, flow):
        try:
            s_packet = IP(packet.ip_packet)
            if s_packet.haslayer(TCP):
                win = s_packet[TCP].window
                if packet.direction == 0 and win > flow.udps.tcp_win_max_in and packet.protocol == 6 :
                    flow.udps.tcp_win_max_in = win
                elif packet.direction == 1 and win > flow.udps.tcp_win_max_out and packet.protocol == 6:
                    flow.udps.tcp_win_max_out = win
                
        except :
            return
