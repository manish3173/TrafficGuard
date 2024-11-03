#!/usr/bin/env python3



from scapy.all import *

import argparse

from collections import Counter



def analyze_packets(pcap_file):

    # Read packets from the pcap file

    packets = rdpcap(pcap_file)



    print(f"\nTotal packets captured: {len(packets)}")



    # Counters to store statistics

    protocol_counter = Counter()

    ip_counter = Counter()



    for packet in packets:

        if IP in packet:

            src_ip = packet[IP].src

            dst_ip = packet[IP].dst

            protocol = packet[IP].proto



            # Count protocols and IP addresses

            protocol_counter[protocol] += 1

            ip_counter[src_ip] += 1

            ip_counter[dst_ip] += 1



    print("\nProtocol Analysis:")

    for proto, count in protocol_counter.items():

        print(f"Protocol {proto} : {count} packets")



    print("\nTop 5 Source IP Addresses:")

    for ip, count in ip_counter.most_common(5):

        print(f"{ip} : {count} packets")



    print("\nTop 5 Destination IP Addresses:")

    for ip, count in ip_counter.most_common(5):

        print(f"{ip} : {count} packets")





if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Analyze network traffic using Scapy")

    parser.add_argument("pcap_file", help="Path to the pcap file captured by tcpdump")



    args = parser.parse_args()



    # Run the analysis

    analyze_packets(args.pcap_file)
