#!/bin/bash

# Network Monitoring System Startup Script

# Set the base directory to the script's location
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$BASE_DIR/src"
CONFIG_DIR="$BASE_DIR/config"
LOG_DIR="$BASE_DIR/logs"
PCAP_DIR="$BASE_DIR/pcaps"

# Configuration
INTERFACE="ethens33"# Change to your network interface (use ifconfig or ip a to find it)
CAPTURE_DURATION=300
METRICS_PORT=8000
PROMETHEUS_PORT=9090
DESTINATIONS="8.8.8.8,1.1.1.1"

echo "Starting Network Monitoring System..."

# Start HAProxy
echo "Starting HAProxy..."
sudo haproxy -f "$CONFIG_DIR/haproxy.cfg" -D -p /var/run/haproxy.pid
echo "HAProxy started"

# Start Metrics Server
echo "Starting Metrics Server on port $METRICS_PORT..."
python3 "$SRC_DIR/metrics_server.py" --port $METRICS_PORT --destinations $DESTINATIONS > "$LOG_DIR/metrics_server.log" 2>&1 &
METRICS_PID=$!
echo "Metrics Server started with PID $METRICS_PID"

# Start Prometheus
echo "Starting Prometheus on port $PROMETHEUS_PORT..."
"$BASE_DIR/bin/prometheus" --config.file="$CONFIG_DIR/prometheus.yml" --storage.tsdb.path="$BASE_DIR/prometheus_data" > "$LOG_DIR/prometheus.log" 2>&1 &
PROMETHEUS_PID=$!
echo "Prometheus started with PID $PROMETHEUS_PID"

# Start Traffic Capture
echo "Starting Traffic Capture on interface $INTERFACE..."
sudo python3 "$SRC_DIR/capture_traffic.py" --interface $INTERFACE --duration $CAPTURE_DURATION --output "$PCAP_DIR/capture_$(date '+%Y%m%d_%H%M%S').pcap" --filter "not port 22" > "$LOG_DIR/capture.log" 2>&1 &
CAPTURE_PID=$!
echo "Traffic Capture started with PID $CAPTURE_PID"

# Register cleanup function
function cleanup {
    echo "Stopping all services..."
    kill $METRICS_PID 2>/dev/null
    kill $PROMETHEUS_PID 2>/dev/null
    kill $CAPTURE_PID 2>/dev/null
    sudo kill -TERM $(cat /var/run/haproxy.pid) 2>/dev/null
    echo "Done."
}

# Register the cleanup function for SIGINT and SIGTERM
trap cleanup SIGINT SIGTERM

echo "All components started. Press Ctrl+C to stop."
echo "Logs are being written to $LOG_DIR"
echo "Traffic captures are being saved to $PCAP_DIR"
echo "Metrics available at: http://localhost:$METRICS_PORT"
echo "Prometheus interface: http://localhost:$PROMETHEUS_PORT"
echo "HAProxy stats: http://localhost:8404/stats"

# Wait for user to press Ctrl+C
wait