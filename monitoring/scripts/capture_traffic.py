#!/usr/bin/env python3

import os

import argparse



def capture_traffic(interface, output_file):

    print(f"Capturing traffic on interface: {interface}")

    command = f"sudo tcpdump -i {interface} -w {output_file}"

    os.system(command)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Capture network traffic using tcpdump.")

    parser.add_argument("interface", help="Network interface to capture traffic on.")

    parser.add_argument("output_file", help="Output pcap file for captured traffic.")

    

    args = parser.parse_args()

    capture_traffic(args.interface, args.output_file)
