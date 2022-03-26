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

# urllib3_connection.allowed_gai_family = allowed_gai_family

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
        if 400 <= r.status_code < 500:
            with open(f".html", "w") as f:
                f.write(r.text)
            return None
        return r
    
    def post(self, params, **kwargs):
        r = super().post(self.server, params, **kwargs)
        if 400 <= r.status_code < 500:
            with open(f".html", "w") as f:
                f.write(r.text)
            return None
        return r

class EtherscanAccount(EtherscanAPI):
    def __init__(self, file, net):
        super().__init__(file, net)
        self.common_params = {"module": "account", "apikey": self.API_key}
    
    def get_address_balance(self, address, **kwargs):
        params = {"action": "balance", "address": address, "tag": "latest"}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return int(r.json()["result"]) / 10 ** 18 if r != None else None

    def get_addresses_balance(self, addresses: list, **kwargs):
        params = {"action": "balancemulti", "tag": "latest", "address": ",".join(addresses)}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return {result["account"]: int(result["balance"]) / 10 ** 18 for result in r.json()["result"]} if r != None else None

    def get_address_normal_transaction(self, address, **kwargs):
        params = {"action": "txlist", "address": address, "startblock": 0, "endblock": 99999999, "page": 1, "offset": 10, "sort": "asc"}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r != None else None

    def get_address_internal_transaction(self, address, **kwargs):
        params = {"action": "txlistinternal", "address": address, "startblock": 0, "endblock": 99999999, "page": 1, "offset": 10, "sort": "asc"}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r != None else None

    def get_internal_transaction_within_block_range(self, start, end, **kwargs):
        params = {"action": "txlistinternal", "startblock": start, "endblock": end, "page": 1, "offset": 10, "sort": "asc"}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r != None else None

    def get_address_erc20_token_transfer_event(self, address, contract_address=None, **kwargs):
        params = {"action": "tokentx", "address": address, "page": 1, "offset": 100, "startblock": 0, "endblock": 27025780, "sort": "asc"}
        params.update(self.common_params)
        if contract_address != None:
            params["contractaddress"] = contract_address
        r = self.get(params, **kwargs)
        return r.json()["result"] if r != None else None

    def get_address_erc721_token_transfer_event(self, address, contract_address=None, **kwargs):
        params = {"action": "tokennfttx", "address": address, "page": 1, "offset": 100, "startblock": 0, "endblock": 27025780, "sort": "asc"}
        params.update(self.common_params)
        if contract_address != None:
            params["contractaddress"] = contract_address
        r = self.get(params, **kwargs)
        return r.json()["result"] if r != None else None

    def get_address_mined_block(self, address, **kwargs):
        params = {"action": "getminedblocks", "address": address, "blocktype": "blocks", "page": 1, "offset": 10}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r != None else None

    def get_address_historical_ether_balance(self, address, **kwargs):
        raise NotImplementedError("This api requires PRO!")

if __name__ == "__main__":
    api = EtherscanAccount("key.json", "mainnet")
    print(api.get_address_mined_block("0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b"))
