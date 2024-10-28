import subprocess
import os
import platform
import speedtest  # For speed test functionality
import logging  # For logging
import socket  # For port scanning
import csv  # For CSV export
import json  # For JSON export

# Setup logging to track diagnostic activities
logging.basicConfig(filename='network_tool.log', level=logging.INFO)

# Global timeout value for commands (in seconds)
TIMEOUT = 10

# This function takes Domain/IP Address to check connectivity to the host
def ping_test():
    host = input("Enter a domain or IP to ping: ")

    # Determine command based on platform
    if os.name == "nt":
        command = ["ping", host]  # Windows uses ping <host>
    else:
        command = ["ping", "-c", "4", host]  # Linux requires '-c' to limit packet count

    try:
        output = subprocess.check_output(command, universal_newlines=True, timeout=TIMEOUT)
        print(output)
        logging.info(f"Ping test for {host}: SUCCESS")
        return output
    except subprocess.TimeoutExpired:
        logging.error(f"Ping test for {host}: TIMEOUT")
        print(f"Ping test timed out after {TIMEOUT} seconds.")
        return ""
    except subprocess.CalledProcessError:
        logging.error(f"Ping test for {host}: FAILED")
        print(f"Failed to reach {host}.")
        return ""

# This function retrieves IP configuration of the system's network interface
def get_ip_configuration():
    if os.name == "nt":
        command = "ipconfig"
    else:
        # For modern Linux systems, 'ip a' is preferred
        command = "ip a" if platform.system() == "Linux" else "ifconfig"  # Fallback to ifconfig for older systems
    
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True, timeout=TIMEOUT)
        print(output)
        logging.info("IP Configuration: SUCCESS")
        return output
    except subprocess.TimeoutExpired:
        logging.error("IP Configuration: TIMEOUT")
        print(f"IP configuration request timed out after {TIMEOUT} seconds.")
        return ""
    except subprocess.CalledProcessError:
        logging.error("IP Configuration: FAILED")
        print("Failed to get IP configuration.")
        return ""

# DNS Lookup function
def dns_lookup():
    domain = input("Enter a domain to resolve: ")
    command = ["nslookup", domain]
    try:
        output = subprocess.check_output(command, universal_newlines=True, timeout=TIMEOUT)
        print(output)
        logging.info(f"DNS lookup for {domain}: SUCCESS")
        return output
    except subprocess.TimeoutExpired:
        logging.error(f"DNS lookup for {domain}: TIMEOUT")
        print(f"DNS lookup timed out after {TIMEOUT} seconds.")
        return ""
    except subprocess.CalledProcessError:
        logging.error(f"DNS lookup for {domain}: FAILED")
        print(f"Failed to resolve {domain}.")
        return ""

# Traceroute function
def traceroute():
    host = input("Enter a domain or IP to trace route: ")

    # Determine the traceroute command based on platform
    command = ["tracert", host] if os.name == "nt" else ["traceroute", host]
    
    try:
        output = subprocess.check_output(command, universal_newlines=True, timeout=TIMEOUT)
        print(output)
        logging.info(f"Traceroute for {host}: SUCCESS")
        return output
    except subprocess.TimeoutExpired:
        logging.error(f"Traceroute for {host}: TIMEOUT")
        print(f"Traceroute timed out after {TIMEOUT} seconds.")
        return ""
    except subprocess.CalledProcessError:
        logging.error(f"Traceroute for {host}: FAILED")
        print(f"Failed to trace route to {host}.")
        dead()

# Internet Speed Test function using speedtest-cli
def run_speed_test():
    print("Running speed test...")
    try:
        st = speedtest.Speedtest()
        st.get_best_server()  # Finds the best server
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        ping_result = st.results.ping  # Ping result
        result = (f"Download Speed: {download_speed:.2f} Mbps\n"
                  f"Upload Speed: {upload_speed:.2f} Mbps\n"
                  f"Ping: {ping_result} ms")
        print(result)
        logging.info("Speed test: SUCCESS")
        return result
    except speedtest.SpeedtestBestServerFailure:
        logging.error("Speed test: TIMEOUT (Failed to find the best server)")
        print(f"Speed test timed out: Failed to find the best server.")
        return ""
    except Exception as e:
        logging.error(f"Speed test: FAILED ({str(e)})")
        print("Speed test failed.")
        return ""

# Port scanning function using socket
def scan_ports():
    host = input("Enter the host IP or domain to scan for open ports: ")
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))

    print(f"Scanning ports {start_port} to {end_port} on {host}...")
    open_ports = []

    try:
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)  # Timeout for each port
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f"Port {port} is open")
                open_ports.append(port)
            sock.close()
        
        if not open_ports:
            print(f"No open ports found on {host} between {start_port} and {end_port}.")
        logging.info(f"Port scan for {host} from {start_port} to {end_port}: {open_ports}")
        return open_ports
    except Exception as e:
        logging.error(f"Port scanning failed: {str(e)}")
        print(f"Port scanning failed: {str(e)}")
        return []

# Save the report to file
def save_report_to_file(data):
    filename = input("Enter the filename to save the report (e.g., report.txt): ")
    try:
        with open(filename, 'w') as file:
            file.write(data)
        print(f"Report saved to {filename}")
        logging.info(f"Report saved to {filename}: SUCCESS")
    except Exception as e:
        logging.error(f"Failed to save report: {str(e)}")
        print(f"Failed to save report: {str(e)}")

# Export report to CSV
def save_report_to_csv(report_data):
    filename = input("Enter the CSV filename (e.g., report.csv): ")
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in report_data.items():
                writer.writerow([key, value])
        print(f"Report saved to {filename}")
        logging.info(f"Report saved to CSV: {filename}")
    except Exception as e:
        logging.error(f"Failed to save CSV: {str(e)}")
        print(f"Failed to save CSV: {str(e)}")

# Export report to JSON
def save_report_to_json(report_data):
    filename = input("Enter the JSON filename (e.g., report.json): ")
    try:
        with open(filename, 'w') as jsonfile:
            json.dump(report_data, jsonfile)
        print(f"Report saved to {filename}")
        logging.info(f"Report saved to JSON: {filename}")
    except Exception as e:
        logging.error(f"Failed to save JSON: {str(e)}")
        print(f"Failed to save JSON: {str(e)}")

# Error handler
def dead():
    print("Task Failed")

# Main function to run the CLI
def main():
    report_data = {}

    while True:
        print("\nWelcome to Network Diagnostic Tool")
        print("-----------------------------------")
        print("1. Ping Test")
        print("2. Get IP Configuration")
        print("3. DNS Lookup")
        print("4. Traceroute")
        print("5. Internet Speed Test")
        print("6. Port Scanning")
        print("7. Save report to file (TXT)")
        print("8. Export report to CSV")
        print("9. Export report to JSON")
        print("10. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            result = ping_test()
            report_data["Ping Test"] = result
        elif choice == '2':
            result = get_ip_configuration()
            report_data["IP Configuration"] = result
        elif choice == '3':
            result = dns_lookup()
            report_data["DNS Lookup"] = result
        elif choice == '4':
            result = traceroute()
            report_data["Traceroute"] = result
        elif choice == '5':
            result = run_speed_test()
            report_data["Speed Test"] = result
        elif choice == '6':
            result = scan_ports()
            report_data["Port Scanning"] = f"Open Ports: {result}"
        elif choice == '7':
            save_report_to_file(str(report_data))
        elif choice == '8':
            save_report_to_csv(report_data)
        elif choice == '9':
            save_report_to_json(report_data)
        elif choice == '10':
            print("Exiting the tool. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
