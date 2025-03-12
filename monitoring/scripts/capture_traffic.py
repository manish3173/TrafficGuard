import subprocess
import time
import psutil
import os
import statistics
import argparse

def capture_traffic(interface='eth0', output_file='capture.pcap', duration=60, threshold=1000, filter_string=''):
    """
    Capture network traffic using tcpdump and monitor traffic volume.
    Calculates traffic rate rather than just volume.
    
    Args:
        interface (str): Network interface to capture from
        output_file (str): Path to save PCAP file
        duration (int): Duration of capture in seconds
        threshold (int): Bytes/sec threshold for traffic spike alerts
        filter_string (str): BPF filter string for tcpdump
    """
    try:
        # Check if running as root
        if os.geteuid() != 0:
            print("Warning: tcpdump requires root privileges. Run with sudo.")
            return

        print(f"Starting traffic capture on {interface} for {duration} seconds...")
        
        # Create directory for pcap files if it doesn't exist
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Build tcpdump command with filter if provided
        command = f"tcpdump -i {interface} -w {output_file} -G {duration}"
        if filter_string:
            command += f" {filter_string}"
        
        print(f"Running: {command}")
        process = subprocess.Popen(command, shell=True)
        
        # Track traffic rates instead of just volume
        previous_bytes = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        rates = []
        
        interval = 5  # Check every 5 seconds
        samples = duration // interval
        
        for i in range(samples):
            time.sleep(interval)
            current_bytes = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            rate = (current_bytes - previous_bytes) / interval  # bytes per second
            rates.append(rate)
            previous_bytes = current_bytes
            
            # Calculate average and standard deviation
            avg_rate = statistics.mean(rates) if rates else 0
            std_dev = statistics.stdev(rates) if len(rates) > 1 else 0
            
            # Better spike detection: current rate > avg + 2*std_dev
            spike_threshold = max(threshold, avg_rate + 2 * std_dev) if len(rates) > 1 else threshold
            
            print(f"[{i+1}/{samples}] Current rate: {rate:.2f} bytes/sec, Avg: {avg_rate:.2f}, Threshold: {spike_threshold:.2f}")
            
            if rate > spike_threshold:
                print(f"ALERT: Traffic spike detected: {rate:.2f} bytes/sec (threshold: {spike_threshold:.2f})")
        
        # Wait for the process to finish
        process.wait()
        print(f"Traffic capture completed. File saved to {output_file}")
        
        # Return summary statistics
        return {
            "average_rate": statistics.mean(rates) if rates else 0,
            "peak_rate": max(rates) if rates else 0,
            "duration": duration
        }
        
    except KeyboardInterrupt:
        print("Capture interrupted.")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"Capture error: {e}")
        if 'process' in locals():
            process.terminate()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Capture network traffic and detect traffic spikes')
    parser.add_argument('--interface', '-i', default='eth0', help='Network interface to capture from')
    parser.add_argument('--output', '-o', default='capture.pcap', help='Output PCAP file path')
    parser.add_argument('--duration', '-d', type=int, default=300, help='Duration of capture in seconds')
    parser.add_argument('--threshold', '-t', type=int, default=1000000, help='Bytes/sec threshold for traffic spike alerts')
    parser.add_argument('--filter', '-f', default='', help='BPF filter string for tcpdump (e.g. "not port 22")')
    
    args = parser.parse_args()
    
    capture_traffic(
        interface=args.interface,
        output_file=args.output,
        duration=args.duration,
        threshold=args.threshold,
        filter_string=args.filter
    )
