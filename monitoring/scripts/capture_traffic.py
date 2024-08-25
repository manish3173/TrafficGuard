import os



def capture_traffic(interface, output_file):

    """Capture network traffic and save it to a file."""

    os.system(f"sudo tcpdump -i {interface} -w {output_file}")



if __name__ == "__main__":

    capture_traffic('enp0s3', 'network_traffic.pcap')