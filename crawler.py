from netmiko import ConnectHandler
import re

"""Class to collect data about network devices and thier connections"""
class Crawler:
    def __init__(self, root):
        self.net_devices = {}
        self.root = root

    def run_crawler_root(self):
        net_connect = ConnectHandler(**self.root)
        root_neigbour_output = net_connect.send_command("ip neighbor/print") #here need to detect what device we are trying to connect to (cisco, huawei ...)
        root_hostname = net_connect.send_command("system identity/print")

        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        mac_pattern = r'(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}'
        interface_pattern = r'(\bether[0-9]+\b)' #maybe we could implement changinf of patterns based on root 'device-type' information
        hostname_pattern = r'name:\s*(\w+)'
        
        interfaces = re.findall(interface_pattern, root_neigbour_output)
        ip_addresses = re.findall(ip_pattern, root_neigbour_output)
        mac_addresses = re.findall(mac_pattern, root_neigbour_output)
        hostname = re.findall(hostname_pattern, root_hostname)

        print(ip_addresses)
        results = {}

        for i in range(len(interfaces)):
            if i < len(ip_addresses):
                results[interfaces[i]] = [ip_addresses[i]]  
            else:
                results[interfaces[i]] = []

        for i in range(len(interfaces)):
            results[interfaces[i]].append(mac_addresses[i]) #what to do if mac addres is not founds

        self.net_devices[hostname[0]] = results

        print(self.net_devices)


    def _run_crawler(self):
        return 0


    def _dev_connect(hostname, username, password):
        #net_connect = ConnectHandler(**mself.root)
        #output = net_connect.send_command('ip address/print')
        #print(output)
        return 0
