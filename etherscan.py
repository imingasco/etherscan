import json
import time
from typing import *
from base import API

SERVER = {
    "mainnet": "https://api.etherscan.io/api",
    "goerli": "https://api-goerli.etherscan.io/api",
    "kovan": "https://api-kovan.etherscan.io/api",
    "rinkeby": "https://api-rinkeby.etherscan.io/api",
    "ropsten": "https://api-ropsten.etherscan.io/api"
}

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
            with open(f"GET_{time.time()}.html", "w") as f:
                f.write(r.text)
            return None
        return r
    
    def post(self, params, **kwargs):
        r = super().post(self.server, params, **kwargs)
        if 400 <= r.status_code < 500:
            with open(f"POST_{time.time()}.html", "w") as f:
                f.write(r.text)
            return None
        return r
