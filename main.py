
from netmiko import ConnectHandler
from crawler import Crawler

mikrotik_1 = {
    'device_type': 'mikrotik_routeros',
    'host': '192.168.126.130',
    'username': 'admin',
    'password': 'admin',
}

def main():
    c = Crawler()
    c.run_crawler(mikrotik_1)
    c.print_net_devices()

if __name__ == "__main__":
    main()