from netmiko import ConnectHandler
import re

"""Class to collect data about network devices and thier connections"""
class Crawler:
    def __init__(self):
        self.net_devices = {}

    def run_crawler(self, net_dev):
        net_connect = ConnectHandler(**net_dev)
        neigbour = net_connect.send_command("ip neighbor/print detail") #here need to detect what device we are trying to connect to (cisco, huawei ...)

        neigbour_splited = neigbour.split('\n')
        neigbour_splited = list(filter(None, neigbour_splited))

        pattern = r'(\S+)=("[^"]*"|\S+)'

        
        if not self.net_devices:
            for c,i in enumerate(neigbour_splited):
                matches = re.findall(pattern, i)
                found_dev = {key: value.strip('"') for key, value in matches}
                if not self._exists(found_dev):
                    self.net_devices[c] = found_dev
        else:
            size = len(self.net_devices)
            for c,i in enumerate(neigbour_splited):
                matches = re.findall(pattern, i)
                found_dev = {key: value.strip('"') for key, value in matches}
                if not self._exists(found_dev):
                    self.net_devices[c] = found_dev
        
        #print(self.net_devices)

        for con in self.net_devices.values():
            if 'address' in con.keys():
                new_net_dev = {
                    'device_type': 'mikrotik_routeros',
                    'username': 'admin',
                    'password': 'admin',
                }
                new_net_dev['host'] = con['address']
                self.run_crawler(new_net_dev)
        

    def _exists(self, found_dev):
        for net_dev in self.net_devices.values():
            if net_dev['identity'] == found_dev['identity']:
                return True
        return False

    def print_net_devices(self):
        print(self.net_devices)