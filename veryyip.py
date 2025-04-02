import socket
import requests
import subprocess
import platform
import os

class VeryyIP:
    def __init__(self):
        pass

    def get(self, ip_type='private'):
        """
        Get the IP address based on the type.
        """
        if ip_type == 'private':
            return self.get_local_ip()
        elif ip_type == 'public':
            return self.get_public_ip()
        else:
            return "Invalid IP type. Use 'private' or 'public'."

    def get_local_ip(self):
        """
        Get the local IP address of the machine.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Connect to a public DNS server
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            return f"Error retrieving local IP: {e}"

    def get_public_ip(self):
        """
        Get the public IP address using an external API.
        """
        try:
            response = requests.get("https://api.ipify.org?format=json")
            if response.status_code == 200:
                return response.json().get("ip")
            else:
                return "Error: Could not retrieve public IP"
        except requests.RequestException as e:
            return f"Error retrieving public IP: {e}"

    def check_ip_status(self):
        """
        Check if the local machine has an IP address.
        """
        local_ip = self.get_local_ip()
        if local_ip:
            return f"Local IP: {local_ip} is assigned."
        else:
            return "No local IP found."

    def set_ip(self, ip_address, netmask='255.255.255.0', gateway='192.168.1.1'):
        """
        Set the IP address of the local machine based on OS.

        ip_address: Desired IP address.
        netmask: Subnet mask (default is '255.255.255.0').
        gateway: Gateway address (default is '192.168.1.1').
        """
        if platform.system() == 'Windows':
            return self.set_ip_windows(ip_address, netmask, gateway)
        elif platform.system() == 'Darwin':  # macOS
            return self.set_ip_mac(ip_address, netmask, gateway)
        elif platform.system() == 'Linux':
            return self.set_ip_linux(ip_address, netmask, gateway)
        else:
            return "Unsupported OS."

    def set_ip_windows(self, ip_address, netmask, gateway):
        """
        Set IP address on Windows.
        """
        try:
            cmd = f"netsh interface ip set address name=\"Ethernet\" static {ip_address} {netmask} {gateway}"
            subprocess.run(cmd, shell=True, check=True)
            return f"IP address set to {ip_address} on Windows."
        except subprocess.CalledProcessError as e:
            return f"Failed to set IP on Windows: {e}"

    def set_ip_mac(self, ip_address, netmask, gateway):
        """
        Set IP address on macOS.
        """
        try:
            cmd = f"sudo ifconfig en0 inet {ip_address} netmask {netmask} up"
            subprocess.run(cmd, shell=True, check=True)
            cmd_gateway = f"sudo route add default {gateway}"
            subprocess.run(cmd_gateway, shell=True, check=True)
            return f"IP address set to {ip_address} on macOS."
        except subprocess.CalledProcessError as e:
            return f"Failed to set IP on macOS: {e}"

    def set_ip_linux(self, ip_address, netmask, gateway):
        """
        Set IP address on Linux.
        """
        try:
            cmd = f"sudo ifconfig eth0 {ip_address} netmask {netmask} up"
            subprocess.run(cmd, shell=True, check=True)
            cmd_gateway = f"sudo route add default gw {gateway}"
            subprocess.run(cmd_gateway, shell=True, check=True)
            return f"IP address set to {ip_address} on Linux."
        except subprocess.CalledProcessError as e:
            return f"Failed to set IP on Linux: {e}"

    def change_dns(self, primary_dns, secondary_dns=None):
        """
        Change DNS settings based on OS.

        primary_dns: Primary DNS address (e.g., '8.8.8.8').
        secondary_dns: Optional secondary DNS address (e.g., '8.8.4.4').
        """
        if platform.system() == 'Windows':
            return self.change_dns_windows(primary_dns, secondary_dns)
        elif platform.system() == 'Darwin':  # macOS
            return self.change_dns_mac(primary_dns, secondary_dns)
        elif platform.system() == 'Linux':
            return self.change_dns_linux(primary_dns, secondary_dns)
        else:
            return "Unsupported OS."

    def change_dns_windows(self, primary_dns, secondary_dns):
        """
        Change DNS on Windows.
        """
        try:
            cmd = f"netsh interface ipv4 set dns name=\"Ethernet\" static {primary_dns}"
            subprocess.run(cmd, shell=True, check=True)
            if secondary_dns:
                cmd_secondary = f"netsh interface ipv4 add dns name=\"Ethernet\" {secondary_dns} index=2"
                subprocess.run(cmd_secondary, shell=True, check=True)
            return f"DNS changed to {primary_dns} (and {secondary_dns if secondary_dns else 'not set'}) on Windows."
        except subprocess.CalledProcessError as e:
            return f"Failed to change DNS on Windows: {e}"

    def change_dns_mac(self, primary_dns, secondary_dns):
        """
        Change DNS on macOS.
        """
        try:
            cmd = f"sudo networksetup -setdnsservers Wi-Fi {primary_dns}"
            subprocess.run(cmd, shell=True, check=True)
            if secondary_dns:
                cmd_secondary = f"sudo networksetup -setdnsservers Wi-Fi {primary_dns} {secondary_dns}"
                subprocess.run(cmd_secondary, shell=True, check=True)
            return f"DNS changed to {primary_dns} (and {secondary_dns if secondary_dns else 'not set'}) on macOS."
        except subprocess.CalledProcessError as e:
            return f"Failed to change DNS on macOS: {e}"

    def change_dns_linux(self, primary_dns, secondary_dns):
        """
        Change DNS on Linux.
        """
        try:
            resolv_conf = '/etc/resolv.conf'
            with open(resolv_conf, 'w') as file:
                file.write(f"nameserver {primary_dns}\n")
                if secondary_dns:
                    file.write(f"nameserver {secondary_dns}\n")
            return f"DNS changed to {primary_dns} (and {secondary_dns if secondary_dns else 'not set'}) on Linux."
        except Exception as e:
            return f"Failed to change DNS on Linux: {e}"

