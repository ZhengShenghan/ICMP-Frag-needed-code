import scapy.all as scapy
import time
if __name__ == "__main__":
    ip = scapy.IP(src='192.168.137.1',dst='192.168.137.209')
    # icmp = scapy.ICMP(type=8)
    tcp = scapy.TCP(sport=24, dport=53)
    icmp = scapy.ICMP()
    count = 0
    host_Ether = '02:00:4c:4f:4f:50'
    ubuntu_Ether = '08:00:27:e0:e3:5a'
    ether = scapy.Ether(src = host_Ether, dst = ubuntu_Ether)
    icmp = scapy.ICMP()
    scapy.sendp(ether/icmp/scapy.Padding('\x00'*1500), iface = '以太网 3')
    '''
    while(1):
        time.sleep(0.05)
        scapy.send(ip/icmp/scapy.Padding('\x00'*1600))
        count += 1
    '''