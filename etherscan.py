import json
import socket
import argparse
import requests.packages.urllib3.util.connection as urllib3_connection
from typing import *
from urllib import request
from base import API

SERVER = {
    "mainnet": "https://api.etherscan.io/api",
    "goerli": "https://api-goerli.etherscan.io/api",
    "kovan": "https://api-kovan.etherscan.io/api",
    "rinkeby": "https://api-rinkeby.etherscan.io/api",
    "ropsten": "https://api-ropsten.etherscan.io/api"
}

def allowed_gai_family():
    """
     https://github.com/shazow/urllib3/blob/master/urllib3/util/connection.py
    """
    family = socket.AF_INET6 if urllib3_connection.HAS_IPV6 else socket.AF_INET
    return family

urllib3_connection.allowed_gai_family = allowed_gai_family

class EtherscanAPI(API):
    def __init__(self, file, net="mainnet"):
        super().__init__()
        self.API_key = self.read_key(file)
        self.net = net
        self.server = SERVER[net]

    def read_key(self, file):
        with open(file, "r") as f:
            data = json.load(f)
        return data["Etherscan"]
    
    def get(self, params, **kwargs):
        r = super().get(self.server, params, **kwargs)
        return r
    
    def post(self, params, **kwargs):
        r = super().post(self.server, params, **kwargs)
        return r


class EtherscanAccount(EtherscanAPI):
    def __init__(self, file, net):
        super().__init__(file, net)
        self.common_params = {"module": "account", "apikey": self.API_key}
    
    def get_address_balance(self, address, **kwargs):
        params = {"action": "balance", "address": address, "tag": "latest"}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        if 400 <= r.status_code < 500:
            with open("balance_error.html", "w") as f:
                f.write(r.text)
            return None
        else:
            return int(r.json()["result"]) // 10 ** 18

    def get_addresses_balance(self, addresses: list, **kwargs):
        params = {"action": "balancemulti", "tag": "latest", "address": ",".join(addresses)}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        ret = {result["account"]: int(result["balance"]) // 10 ** 18 for result in r.json()["result"]}
        return ret

    def get_address_transaction(self, address, **kwargs):
        params = {"action": "txlist", "address": address, "startblock": 0, "endblock": 99999999, "page": 1, "offset": 10, "sort": "asc"}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"]

if __name__ == "__main__":
    api = EtherscanAccount("key.json", "kovan")
    print(api.get_address_balance("0x1a96b417224F4bEf2C4708f04fa801Af9fAc6D45"))