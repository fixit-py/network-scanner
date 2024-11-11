import socket
import struct
import time
import os

def checksum(data):
    s = 0
    for i in range(0, len(data), 2):
        w = (data[i] << 8) + (data[i + 1] if (i + 1) < len(data) else 0)
        s = (s + w) & 0xffff
    s = ~s & 0xffff
    return s

def raw_ping(target_ip):
    icmp_type = 8  # ICMP Echo Request
    icmp_code = 0
    packet_id = os.getpid() & 0xFFFF
    sequence = 1
    header = struct.pack('!BBHHH', icmp_type, icmp_code, 0, packet_id, sequence)
    payload = b'Ping'
    checksum_value = checksum(header + payload)
    header = struct.pack('!BBHHH', icmp_type, icmp_code, checksum_value, packet_id, sequence)
    packet = header + payload

    # Open raw socket
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
        sock.settimeout(1)
        start_time = time.time()
        sock.sendto(packet, (target_ip, 1))

        try:
            data, _ = sock.recvfrom(1024)
            end_time = time.time()
            print(f"Reply from {target_ip}: time={(end_time - start_time) * 1000:.2f}ms")
        except socket.timeout:
            print("Request timed out")

i=0
while i<10000:
    raw_ping("8.8.8.8")
    i-=1
