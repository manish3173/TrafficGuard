# TrafficGuard : A comprehensive system for monitoring and optimizing network traffic
## Overview

This project provides a comprehensive system for monitoring and optimizing network traffic. It includes tools for capturing network traffic, analyzing it, and optimizing traffic flow using HAProxy. Performance is monitored with Prometheus and Grafana.

## Installation on Ubuntu
### Cloning the Repository

1. **Clone the Repository**
   ```bash
   git clone https://github.com/manish3173/TrafficGuard.git
   cd TrafficGuard


### Monitoring

1. **tcpdump**: Captures network traffic.
   - Install tcpdump using the following command:
     ```bash
     sudo apt update
     sudo apt install tcpdump
     ```
  
### Analysis

1. **Scapy**: Analyzes network traffic.
   - Install Scapy using pip:
     ```bash
     sudo apt update
     sudo apt install python3-pip
     pip3 install scapy
     ```
 

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
 .

2. **Grafana**: Visualizes metrics collected by Prometheus.
   - Install Grafana:
     ```bash
     sudo apt update
     sudo apt install -y software-properties-common
     sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
     sudo apt update
     sudo apt install grafana
     ```
 

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


## Contributing

Feel free to submit issues and pull requests. Contributions are welcome!

## Contact

For questions or support, please contact:

- **Y Manish Kumar**: [ymanishk602@gmail.com](mailto:ymanishk602@gmail.com)


## Acknowledgements

- [tcpdump](https://www.tcpdump.org/)
- [Scapy](https://scapy.net/)
- [HAProxy](http://www.haproxy.org/)
- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)
