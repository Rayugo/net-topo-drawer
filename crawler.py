from netmiko import ConnectHandler
import re
from time import sleep
from pprint import pprint

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

#zrobic zmienna przechowujaca obecne urzadzenie z ktorym jestesmy polaczeni

#jesli nowo dodane 'connection' posiada 'identity' urzadzenia ktore
#juz istnieje R1, R2 itp. to dodaj to 'connection' ale nie lacz sie znim

#czy software-id identyfikuje unikalnie urzadzenie ? czy zostac przy identity?


"""Class to collect data about network devices and thier connections"""
class Crawler:
    def __init__(self):
        self.net_devices = {}
        self.curr_net_dev = None
        self.pattern_neighbour = r'(\S+)=("[^"]*"|\S+)'
        self.pattern_identity = r'name: (\S+)'

    def run_crawler(self, net_dev):
        print(f"Connecting to {net_dev['host']} ...")
        self.curr_net_de = net_dev
        net_connect = ConnectHandler(**net_dev)
        neighbour = net_connect.send_command("ip neighbor/print detail") #here need to detect what device we are trying to connect to (cisco, huawei ...)
        identity = net_connect.send_command("system identity/print")
        neighbour_splited = neighbour.split('\n')
        neighbour_splited = list(filter(None, neighbour_splited))
        identity = re.search(self.pattern_identity,identity) #dodac moze jakis warunek gdyby nie znalazlo identity
        identity = identity.group(1)
        
        #adding found connections to neighbouring net devices
        self.net_devices[identity] = {'connections': {} }
        for c,i in enumerate(neighbour_splited):
            matches = re.findall(self.pattern_neighbour, i)
            found_con = {key: value.strip('"') for key, value in matches}
            self.net_devices[identity]['connections'][c] = found_con

        curr_net_devices = self.net_devices #PROBLEM Z REKURSJA !!! SPROBOWAC INNE ROZWIAZANIE
        
        #trying to connect to neighbouring devices that do not exist in self.net_devices
        for net_dev in curr_net_devices.values():
            for con in net_dev['connections'].values():
                if not self._exists(con['identity']) and 'address' in con.keys():
                    new_net_dev = {
                        'device_type': 'mikrotik_routeros',
                        'username': 'admin',
                        'password': 'admin',
                    }
                    #print(con)
                    new_net_dev['host'] = con['address']
                    self.run_crawler(new_net_dev) #start recursive search until no new devices found
        
    #need to add detecting looping e.x 172.16.0.1 -> 172.16.0.2 -> 172.16.0.1 ...
    def _exists(self, found_con_idenity):
        for identity in self.net_devices.keys():
            if identity == found_con_idenity:
                return True
        return False

    def print_net_devices(self):
        print(self.net_devices)