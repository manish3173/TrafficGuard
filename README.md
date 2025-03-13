# TrafficGuard : A comprehensive system for monitoring and optimizing network traffic

This project provides a comprehensive system for monitoring and optimizing network traffic. It includes tools for capturing network traffic, analyzing it, and optimizing traffic flow using HAProxy. Performance is monitored with Prometheus and Grafana.

## Installation on Ubuntu

### Step-by-Step Installation
1. Clone the Repository
   ```bash
   git clone https://github.com/manish3173/TrafficGuard.git
   cd TrafficGuard
   ```
2. Install Monitoring Tools
   ```bash
   sudo apt update
   sudo apt install tcpdump -y
   ```
3. Install Analysis Tools
   ```bash
   sudo apt install python3-pip -y
   pip3 install scapy prometheus-client psutil
   ```
4. Install Optimization Tools
   ```bash
   sudo apt install haproxy -y
   cp config/haproxy.cfg /etc/haproxy/haproxy.cfg
   sudo systemctl restart haproxy
   ```
5. Install Reporting Tools
   ```bash
   # Install Prometheus
   wget https://github.com/prometheus/prometheus/releases/download/v2.43.0/prometheus-2.43.0.linux-amd64.tar.gz
   tar xvf prometheus-2.43.0.linux-amd64.tar.gz
   mv prometheus-2.43.0.linux-amd64 /opt/prometheus

   # Install Grafana
   sudo apt update
   sudo apt install -y software-properties-common
   sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
   sudo apt update
   sudo apt install grafana -y
   sudo systemctl start grafana-server
   ```

## Usage
- Start the Monitoring System
  ```bash
  ./start_monitor.sh
  ```

- Capture Traffic Manually
  ```bash
  sudo python3 src/capture_traffic.py --interface enp0s3 --duration 300 --output pcaps/capture_manual.pcap --filter "not port 22"
  ```
- Analyze Captured Traffic
  ```bash
  sudo python3 src/analyze_traffic.py pcaps/capture_manual.pcap
  ```
- Start Metrics Server
  ```bash
  sudo python3 src/metrics_server.py --port 8000 --destinations 8.8.8.8,1.1.1.1
  ```
- Start Prometheus
  ```bash
  sudo prometheus --config.file=config/prometheus.yml --storage.tsdb.path=prometheus_data
  ```
- Access Monitoring Interfaces
  - Metrics Server: http://localhost:8000
  - Prometheus: http://localhost:9090
  - HAProxy Stats: http://localhost:8404/stats (username: admin, password: adminpassword)

## Configuration
### HAProxy Configuration
Edit `config/haproxy.cfg` to:
- Add backend servers if needed
- Modify load balancing algorithms as required
- Configure health checks
- Set security parameters

### Prometheus Configuration
Modify `config/prometheus.yml` to:
- Add additional monitoring targets if you want more servers
- Configure alerting rules
- Adjust scraping intervals

### Connecting Grafana to Prometheus
1. Log in to Grafana at http://localhost:3000.
2. Go to the Configuration (gear icon) > Data Sources > Add data source.
3. Search for Prometheus, select it, and configure:
   - Name: Prometheus
   - URL: http://localhost:9090
   - Access: Browser
   - Scrape Interval: 15s
4. Click Save & Test to verify the connection.

### Creating a Dashboard in Grafana
1. Click the "+" icon in the sidebar and select Dashboard.
2. Click Add new panel.
3. In the Metrics tab, click Add query.
4. Select the Prometheus data source and enter a PromQL query to visualize your metrics.

## Contributing
Feel free to submit issues and pull requests. Contributions are welcome!

## Contact
For questions or support, please contact:

- **Y Manish Kumar**: [ymanishk602@gmail.com](mailto:ymanishk602@gmail.com)

## License
This project is licensed under the MIT License.
