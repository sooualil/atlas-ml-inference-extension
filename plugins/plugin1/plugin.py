from scapy.all import IP, TCP, DNS, DNSRR

class AuxPktMinMaxSizeFeatures(NFPlugin):

    def on_init(self, packet, flow):
        flow.udps.min_ttl = 100000
        flow.udps.max_ttl = -100000
        flow.udps.min_ip_pkt_len = 100000
        flow.udps.max_ip_pkt_len = -100000
        flow.udps.longest_flow_pkt = -100000
        flow.udps.shortest_flow_pkt = 100000
        curr_flag = -1
        try:
            if packet.ip_version == 4:
                decoded_packet = dpkt.ip.IP(packet.ip_packet)
                lenght = decoded_packet.len
                ttl = decoded_packet.ttl
                if packet.protocol == 6:
                    curr_flag = decoded_packet.data.flags
                    curr_flag = curr_flag


            elif packet.ip_version == 6:
                decoded_packet = dpkt.ip6.IP6(packet.ip_packet)
                lenght = decoded_packet.plen + 40
                ttl = decoded_packet.hlim
                if packet.protocol == 6:
                    curr_flag = decoded_packet.data.flags
                    curr_flag = curr_flag

        except:
            return
        flow.udps.min_ip_pkt_len = lenght
        flow.udps.max_ip_pkt_len = lenght
        
        flow.udps.longest_flow_pkt = packet.raw_size
        flow.udps.shortest_flow_pkt = packet.raw_size
        
        flow.udps.min_ttl = ttl
        flow.udps.max_ttl = ttl
        
        if curr_flag != -1:
            flow.udps.tcp_flags = curr_flag
        if packet.direction == 0:
            flow.udps.src2dst_flags = curr_flag
        else:
            flow.udps.dst2src_flags = curr_flag
            

    def on_update(self, packet, flow):
        try:
            if packet.ip_version == 4:
                decoded_packet = dpkt.ip.IP(packet.ip_packet)
                lenght = decoded_packet.len
                ttl = decoded_packet.ttl

            elif packet.ip_version == 6:
                decoded_packet = dpkt.ip6.IP6(packet.ip_packet)
                lenght = decoded_packet.plen + 40
                ttl = decoded_packet.hlim

        except:
            return
                
        if ttl < flow.udps.min_ttl:
            flow.udps.min_ttl = ttl
        elif ttl > flow.udps.max_ttl:
            flow.udps.max_ttl = ttl
        
        if lenght < flow.udps.min_ip_pkt_len:
            flow.udps.min_ip_pkt_len = lenght
        elif lenght > flow.udps.max_ip_pkt_len:
            flow.udps.max_ip_pkt_len = lenght
        
        if packet.raw_size < flow.udps.shortest_flow_pkt:
            flow.udps.shortest_flow_pkt = packet.raw_size
        elif packet.raw_size > flow.udps.longest_flow_pkt:
            flow.udps.longest_flow_pkt = packet.raw_size
        

