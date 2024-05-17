from crawler import Crawler
from gui_interface import GuiInterface

mikrotik_1 = {
    'device_type': 'mikrotik_routeros',
    'host': '192.168.19.129',
    'username': 'admin',
    'password': 'admin',
}


def main():
    c = Crawler()
    c.run_crawler(mikrotik_1)
    c.print_net_devices()
    g = GuiInterface(c.get_net_devices())


if __name__ == "__main__":
    main()
