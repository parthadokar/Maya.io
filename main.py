import subprocess
import os
import platform

# This function takes Domain/IP Address to check connectivity to the host
def ping_test():
    host = input("Enter a domain or IP to ping: ")
    
    # Determine command based on platform
    if os.name == "nt":
        command = ["ping", host]  # Windows uses ping <host>
    else:
        command = ["ping", "-c", "4", host]  # Linux requires '-c' to limit packet count

    try:
        output = subprocess.check_output(command, universal_newlines=True)
        print(output)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Failed to reach {host}. Error : {str(e)}")
        return ""

# This function retrieves IP configuration of the system's network interface
def get_ip_configuration():
    if os.name == "nt":
        command = "ipconfig"
    else:
        # For modern Linux systems, 'ip a' is preferred
        if platform.system() == "Linux":
            command = "ip a"  
        else:
            command = "ifconfig"  # Fallback to ifconfig for older Unix-based systems
    
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        print(output)
        return output
    except subprocess.CalledProcessError as e:
        print("Failed to get IP configuration. Error : {str(e)}")
        return ""

# DNS Lookup function
def dns_lookup():
    domain = input("Enter a domain to resolve: ")
    command = ["nslookup", domain]
    try:
        output = subprocess.check_output(command, universal_newlines=True,timeout=5)
        print(output)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Failed to resolve {domain}. Error : {str(e)}")
        return ""

# Traceroute function
def traceroute():
    host = input("Enter a domain or IP to trace route: ")
    
    # Determine the traceroute command based on platform
    if os.name == "nt":
        command = ["tracert", host]  # Windows uses tracert
    else:
        command = ["traceroute", host]  # Linux uses traceroute
    
    try:
        output = subprocess.check_output(command, universal_newlines=True)
        print(output)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Failed to trace route to {host}. Error : {str(e)}")
        dead()

# Save the report to file
def save_report_to_file(data):
    filename = input("Enter the filename to save the report (e.g., report.txt): ")
    with open(filename, 'w') as file:
        file.write(data)
    print(f"Report saved to {filename}")

# Error handler
def dead():
    print("Task Failed")

# Main function to run the CLI
def main():
    report_data = ""

    while True:
        print("\nWelcome to Network Diagnostic Tool")
        print("-----------------------------------")
        print("1. Ping Test")
        print("2. Get IP Configuration")
        print("3. DNS Lookup")
        print("4. Traceroute")
        print("5. Save report to file")
        print("6. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            result = ping_test()
            report_data += f"\nPing Test Result:\n{result}"
        elif choice == '2':
            result = get_ip_configuration()
            report_data += f"\nIP Configuration Result:\n{result}"
        elif choice == '3':
            result = dns_lookup()
            report_data += f"\nDNS Lookup Result:\n{result}"
        elif choice == '4':
            result = traceroute()
            report_data += f"\nTraceroute Result:\n{result}"
        elif choice == '5':
            save_report_to_file(report_data)
        elif choice == '6':
            print("Exiting the tool. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
