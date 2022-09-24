import scapy.all as scapy
import time
if __name__ == "__main__":
    # unable to generate ping
    host = '192.168.137.1'
    ubuntu_VM = '192.168.137.209'
    windows_VM = '192.168.137.67'
    gateway = '192.168.137.1'
    blackhole = '1.2.3.4'
    host_Ether = '02:00:4c:4f:4f:50'
    ubuntu_Ether = '08:00:27:e0:e3:5a'
    windows_Ether = '08:00:27:ee:16:f3'
    ether = scapy.Ether(src = host_Ether, dst = ubuntu_Ether)
    ip = scapy.IP(src = gateway ,dst = ubuntu_VM)
    icmp = scapy.ICMP()
    count = 0
    while(1):
        time.sleep(0.05)
        scapy.sendp(ether/ip/icmp/scapy.Padding('\x00'*1500), iface = '以太网 3')
        count += 1
        print(count)
   

