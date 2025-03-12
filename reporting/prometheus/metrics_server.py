from prometheus_client import start_http_server, Counter, Gauge
import psutil
import time
import socket
import subprocess
import threading
import argparse

# Metrics definitions
NETWORK_BYTES_SENT = Counter('network_bytes_sent_total', 'Total network bytes sent')
NETWORK_BYTES_RECV = Counter('network_bytes_recv_total', 'Total network bytes received')
PACKET_SENT = Counter('network_packets_sent_total', 'Total packets sent')
PACKET_RECV = Counter('network_packets_recv_total', 'Total packets received')
LATENCY = Gauge('network_latency_ms', 'Network latency in ms', ['destination'])
PACKET_LOSS = Gauge('network_packet_loss_percent', 'Percentage of packets lost', ['destination'])
CONNECTIONS = Gauge('network_connections', 'Number of network connections', ['state'])

# Global variables for tracking
prev_bytes_sent = 0
prev_bytes_recv = 0
prev_packets_sent = 0
prev_packets_recv = 0

def get_network_stats():
    """Retrieve system network metrics"""
    try:
        net = psutil.net_io_counters()
        return net.bytes_sent, net.bytes_recv, net.packets_sent, net.packets_recv
    except Exception as e:
        print(f"Error getting network stats: {e}")
        return 0, 0, 0, 0

def measure_latency(host="8.8.8.8"):
    """Measure actual network latency using ping"""
    try:
        # Use ping to measure actual latency
        ping_cmd = f"ping -c 3 {host}"
        result = subprocess.run(ping_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Parse the ping output for latency
            for line in result.stdout.split('\n'):
                if "avg" in line:
                    # Extract the average latency
                    parts = line.split('/')
                    if len(parts) >= 5:
                        avg_latency = float(parts[4])
                        return avg_latency, 0  # Return latency and 0% packet loss
        
        # If ping fails, assume 100% packet loss
        return 0, 100
    except Exception as e:
        print(f"Error measuring latency: {e}")
        return 0, 0

def update_connection_metrics():
    """Update connection counts by state"""
    try:
        # Get all connections
        connections = psutil.net_connections()
        
        # Count by state
        states = {}
        for conn in connections:
            state = conn.status if conn.status else "NONE"
            states[state] = states.get(state, 0) + 1
        
        # Update gauges
        for state, count in states.items():
            CONNECTIONS.labels(state=state).set(count)
    except Exception as e:
        print(f"Error updating connection metrics: {e}")

def latency_monitor(destinations, interval=60):
    """Monitor latency to multiple destinations in a separate thread"""
    while True:
        for dest in destinations:
            try:
                latency, loss = measure_latency(dest)
                LATENCY.labels(destination=dest).set(latency)
                PACKET_LOSS.labels(destination=dest).set(loss)
            except Exception as e:
                print(f"Error monitoring {dest}: {e}")
        time.sleep(interval)

def update_metrics(interval=5):
    """Update all metrics periodically"""
    global prev_bytes_sent, prev_bytes_recv, prev_packets_sent, prev_packets_recv
    
    while True:
        try:
            # Get current network stats
            bytes_sent, bytes_recv, packets_sent, packets_recv = get_network_stats()
            
            # Calculate differences
            bytes_sent_diff = bytes_sent - prev_bytes_sent
            bytes_recv_diff = bytes_recv - prev_bytes_recv
            packets_sent_diff = packets_sent - prev_packets_sent
            packets_recv_diff = packets_recv - prev_packets_recv
            
            # Update counters properly
            if bytes_sent_diff > 0:
                NETWORK_BYTES_SENT.inc(bytes_sent_diff)
            if bytes_recv_diff > 0:
                NETWORK_BYTES_RECV.inc(bytes_recv_diff)
            if packets_sent_diff > 0:
                PACKET_SENT.inc(packets_sent_diff)
            if packets_recv_diff > 0:
                PACKET_RECV.inc(packets_recv_diff)
            
            # Update connection metrics
            update_connection_metrics()
            
            # Update previous values
            prev_bytes_sent = bytes_sent
            prev_bytes_recv = bytes_recv
            prev_packets_sent = packets_sent
            prev_packets_recv = packets_recv
            
            time.sleep(interval)
        except Exception as e:
            print(f"Error updating metrics: {e}")
            time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Network metrics exporter for Prometheus')
    parser.add_argument('--port', type=int, default=8000, help='Port to expose metrics on')
    parser.add_argument('--interval', type=int, default=5, help='Metrics update interval in seconds')
    parser.add_argument('--destinations', default='8.8.8.8,1.1.1.1', help='Comma-separated list of destinations to monitor latency')
    args = parser.parse_args()
    
    # Parse destinations
    destination_list = [d.strip() for d in args.destinations.split(',')]
    
    try:
        # Start HTTP server for metrics
        start_http_server(args.port)
        print(f"Metrics server started on port {args.port}")
        
        # Start latency monitoring in a separate thread
        latency_thread = threading.Thread(
            target=latency_monitor, 
            args=(destination_list, args.interval * 6),  # Monitor latency less frequently
            daemon=True
        )
        latency_thread.start()
        
        # Start main metrics update loop
        print(f"Starting metrics collection with {args.interval}s interval")
        print(f"Monitoring latency to: {', '.join(destination_list)}")
        update_metrics(args.interval)
    except KeyboardInterrupt:
        print("Stopping metrics server...")
    except Exception as e:
        print(f"Error starting metrics server: {e}")
