# TrafficGuard

**TrafficGuard** is a comprehensive system for monitoring and optimizing network traffic. It includes tools for capturing network traffic, analyzing it, and optimizing traffic flow using HAProxy. Performance is monitored with Prometheus and Grafana.

## Overview

This project provides a comprehensive system for monitoring and optimizing network traffic. It includes tools for capturing network traffic, analyzing it, and optimizing traffic flow using HAProxy. Performance is monitored with Prometheus and Grafana.

## Installation on Ubuntu

### Monitoring

1. **tcpdump**: Captures network traffic.
   - Install tcpdump using the following command:
     ```bash
     sudo apt update
     sudo apt install tcpdump
     ```
   - Follow the detailed installation guide [here](monitoring/tcpdump/installation_guide.md).

### Analysis

1. **Scapy**: Analyzes network traffic.
   - Install Scapy using pip:
     ```bash
     sudo apt update
     sudo apt install python3-pip
     pip3 install scapy
     ```
   - See the installation guide [here](analysis/scapy/installation_guide.md).

### Optimization

1. **HAProxy**: For load balancing and traffic optimization.
   - Install HAProxy:
     ```bash
     sudo apt update
     sudo apt install haproxy
     ```
   - Configure HAProxy using the provided [haproxy.cfg](optimization/haproxy/haproxy.cfg).

### Reporting

1. **Prometheus**: Collects metrics for performance monitoring.
   - Download and install Prometheus:
     ```bash
     wget https://github.com/prometheus/prometheus/releases/download/v2.43.0/prometheus-2.43.0.linux-amd64.tar.gz
     tar xvf prometheus-2.43.0.linux-amd64.tar.gz
     cd prometheus-2.43.0.linux-amd64
     ```
   - Follow the installation and configuration guide [here](reporting/prometheus/installation_guide.md).

2. **Grafana**: Visualizes metrics collected by Prometheus.
   - Install Grafana:
     ```bash
     sudo apt update
     sudo apt install -y software-properties-common
     sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
     sudo apt update
     sudo apt install grafana
     ```
   - Set up Grafana following the guide [here](reporting/grafana/installation_guide.md).

## Usage

1. **Capture Network Traffic**
   - Run `capture_traffic.py` to start capturing network packets:
     ```bash
     python3 capture_traffic.py
     ```

2. **Analyze Traffic**
   - Use `analysis_script.py` to analyze the captured data:
     ```bash
     python3 analysis_script.py
     ```

3. **Optimize Traffic**
   - Configure HAProxy using `haproxy.cfg` and start it:
     ```bash
     sudo systemctl restart haproxy
     ```

4. **Monitor Performance**
   - Configure Prometheus and Grafana to monitor and visualize performance metrics.

## Troubleshooting

For common issues and solutions, refer to [troubleshooting.md](docs/troubleshooting.md).

## Contributing

Feel free to submit issues and pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [tcpdump](https://www.tcpdump.org/)
- [Scapy](https://scapy.net/)
- [HAProxy](http://www.haproxy.org/)
- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)
