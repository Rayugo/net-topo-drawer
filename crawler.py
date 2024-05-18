from netmiko import ConnectHandler
import re
from time import sleep
from pprint import pprint
from copy import copy

"""
self.net_devices = {
    ROOT: {
        connections: {
            0: ...
            1: ...
        },
        addresses: {
            0: ...
            1: ...
        },
        ...
    },
    R1: {
        connections: {
            0: ...
            1: ...
        },
        addresses: {
            0: ...
            1: ...
        },
        ...
    },
}

"""

# czy software-id identyfikuje unikalnie urzadzenie ? czy zostac przy identity?


"""Class to collect data about network devices and their connections"""


class Crawler:
    def __init__(self):
        self.net_devices = {}
        self.platforms = {'mikrotik_routeros': {'get_hostname': 'system identity/print',
                                                'get_neighbors': 'ip neighbor/print detail'
                                                },
                          'cisco_ios': {'get_hostname': 'show running-config | include hostname',
                                        'get_neighbors': 'show lldp neighbors detail', }
                          }
        self.curr_net_dev = None

    def run_crawler(self, net_dev):
        print(f"Connecting to {net_dev['host']} ...")
        self.curr_net_dev = net_dev
        self._get_device_data(self.curr_net_dev['device_type'])

        curr_net_devices = self.net_devices.copy()  # need to do copy because of recursive search

        # trying to connect to neighbouring devices that do not exist in self.net_devices
        for net_dev in curr_net_devices.values():
            for con in net_dev['connections'].values():
                if not self._exists(con[
                                        'identity']) and 'address' in con.keys():  # need to correct condition to match different products
                    self.run_crawler(self._create_new_net_dev(con))  # start recursive search until no new devices found

    def _exists(self, found_con_identity):
        for identity in self.net_devices.keys():
            if identity == found_con_identity:
                return True
        return False

    def print_net_devices(self):
        pprint(self.net_devices)

    def get_net_devices(self):
        return self.net_devices

    def _get_device_data(self, device_type):
        net_connect = ConnectHandler(**self.curr_net_dev)
        if device_type == 'mikrotik_routeros':
            neighbour = net_connect.send_command(
                "ip neighbor/print detail")  # here need to detect what device we are trying to connect to (cisco, huawei ...)
            identity = net_connect.send_command("system identity/print")
            neighbour_pattern = r'(\S+)=("[^"]*"|\S+)'  # here we need to change the pattern based on device type
            identity_pattern = r'name: (\S+)'
            neighbour_split = neighbour.split('\n')
            neighbour_split = list(filter(None, neighbour_split))
            identity = re.search(identity_pattern, identity)
            identity = identity.group(1)

            # adding found connections to neighbouring net devices
            self.net_devices[identity] = {}
            self.net_devices[identity]['device_type'] = 'mikrotik_routeros'
            self.net_devices[identity]['connections'] = {}
            for c, i in enumerate(neighbour_split):
                matches = re.findall(neighbour_pattern, i)
                found_con = {key: value.strip('"') for key, value in matches}
                self.net_devices[identity]['connections'][c] = found_con
        elif device_type == 'cisco_ios':
            neighbour = net_connect.send_command(self.platforms['cisco']['get_neighbors'])
            identity = net_connect.send_command(self.platforms['cisco']['get_hostname'])

    def _create_new_net_dev(self, con):
        #print(con)
        device_type = self._get_device_type(con)
        new_net_dev = {'device_type': 'mikrotik_routeros', 'username': 'admin', 'password': 'admin',
                       'host': con['address']}
        return new_net_dev

    def _get_device_type(self, con):
        print(con['version'])
