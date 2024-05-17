from crawler import Crawler
from gui_interface import GuiInterface
import threading


class Controller:
    def __init__(self):
        self.net_devices = {}
        self.view = GuiInterface(self)  # GuiInterface w głównym wątku
        print("Instancja GuiInterface została przypisana do self.view")

    def start_crawler(self):
        mikrotik_1 = {
            'device_type': 'mikrotik_routeros',
            'host': '192.168.126.130',
            'username': 'admin',
            'password': 'admin',
        }
        threading.Thread(target=self.run_crawler, args=(mikrotik_1,)).start()

    def start_gui(self):
        self.view.root.mainloop()

    def run_crawler(self, device_info):
        try:
            c = Crawler()
            c.run_crawler(device_info)
            self.net_devices = c.get_net_devices()
            self.view.root.after(0, self.view.update_graph, self.net_devices)  # Aktualizuj GUI
        except Exception as e:
            self.view.root.after(0, self.view.show_error, f"An error occurred: {str(e)}")
