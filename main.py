#from nornir import InitNornir
#from nornir.core.plugins.connections import ConnectionPlugin
#from nornir_routeros.plugins.tasks import routeros_get
#from nornir.core.task import Task, Result
#from nornir_utils.plugins.functions import print_result

from netmiko import ConnectHandler
from crawler import Crawler

""""
def main():
    print("Running 'main' ...")
    nr = InitNornir(config_file="config.yaml")
    result = nr.run(
        task=routeros_get,
        path="/ip/address"
    )
    print_result(result)
"""

mikrotik_1 = {
    'device_type': 'mikrotik_routeros',
    'host': '192.168.126.130',
    'username': 'admin',
    'password': 'admin',
}

def main():
    c = Crawler(mikrotik_1)
    c.run_crawler_root()

if __name__ == "__main__":
    main()