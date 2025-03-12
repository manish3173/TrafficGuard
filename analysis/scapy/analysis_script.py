from scapy.all import rdpcap, IP, TCP, UDP
from collections import defaultdict
import argparse
import os

# Extended list of unusual protocols with descriptions
UNUSUAL_PROTOCOLS = {
    47: "GRE (Generic Routing Encapsulation)",
    50: "ESP (Encapsulating Security Payload)",
    51: "AH (Authentication Header)",
    41: "IPv6 Encapsulation",
    58: "ICMPv6",
    89: "OSPF",
    103: "PIM (Protocol Independent Multicast)",
    112: "VRRP (Virtual Router Redundancy Protocol)"
}

def analyze_traffic(pcap_file, output_file=None):
    """
    Analyze PCAP file for protocols and anomalies with improved detection
    """
    if not os.path.exists(pcap_file):
        print(f"Error: PCAP file {pcap_file} not found")
        return
    
    try:
        print(f"Loading packets from {pcap_file}...")
        packets = rdpcap(pcap_file)
        
        stats = {
            'total_packets': len(packets),
            'protocols': defaultdict(int),
            'unusual_protocols': defaultdict(int),
            'oversized_packets': defaultdict(int),
            'port_distribution': defaultdict(int),
            'tcp_flags': defaultdict(int),
            'ip_count': defaultdict(int)
        }
        
        # Standard MTU size
        MTU = 1500
        
        print(f"Analyzing {len(packets)} packets...")
        for pkt in packets:
            if IP in pkt:
                ip_src = pkt[IP].src
                ip_dst = pkt[IP].dst
                protocol = pkt[IP].proto
                
                # Count IPs for frequency analysis
                stats['ip_count'][ip_src] += 1
                
                # Protocol distribution
                stats['protocols'][protocol] += 1
                
                # Unusual protocol detection
                if protocol in UNUSUAL_PROTOCOLS:
                    stats['unusual_protocols'][protocol] += 1
                
                # Oversized packet detection
                if pkt[IP].len > MTU:
                    stats['oversized_packets'][ip_src] += 1
                
                # Port distribution for TCP/UDP
                if TCP in pkt:
                    stats['port_distribution'][f"TCP:{pkt[TCP].dport}"] += 1
                    # TCP flags analysis
                    flags = pkt[TCP].flags
                    stats['tcp_flags'][flags] += 1
                elif UDP in pkt:
                    stats['port_distribution'][f"UDP:{pkt[UDP].dport}"] += 1
        
        # Output results
        print(f"\n=== Analysis Results for {pcap_file} ===")
        print(f"Total packets: {stats['total_packets']}")
        
        print("\nProtocol Distribution:")
        for proto, count in sorted(stats['protocols'].items(), key=lambda x: x[1], reverse=True):
            protocol_name = {1: "ICMP", 6: "TCP", 17: "UDP"}.get(proto, f"Protocol {proto}")
            print(f"  {protocol_name}: {count} packets ({count/stats['total_packets']*100:.1f}%)")
        
        print("\nUnusual Protocol Usage:")
        for proto, count in stats['unusual_protocols'].items():
            print(f"  {UNUSUAL_PROTOCOLS.get(proto, f'Protocol {proto}')}: {count} packets")
        
        print("\nTop 5 Destination Ports:")
        for port, count in sorted(stats['port_distribution'].items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {port}: {count} packets")
        
        print("\nPotential Anomalies:")
        
        # Oversized packets
        if stats['oversized_packets']:
            print("  Oversized Packets (> MTU):")
            for ip, count in sorted(stats['oversized_packets'].items(), key=lambda x: x[1], reverse=True):
                print(f"    {ip}: {count} packets")
        
        # Write output to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(f"Analysis Results for {pcap_file}\n")
                f.write(f"Total packets: {stats['total_packets']}\n")
                # Additional output formatting would go here
        
        return stats
        
    except Exception as e:
        print(f"Analysis error: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze PCAP traffic files')
    parser.add_argument('pcap_file', help='Path to PCAP file')
    parser.add_argument('-o', '--output', help='Output file for analysis results')
    args = parser.parse_args()
    
    analyze_traffic(args.pcap_file, args.output)
