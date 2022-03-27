from etherscan import EtherscanAPI


class EtherscanTransaction(EtherscanAPI):
    def __init__(self, file, net="mainnet"):
        super().__init__(file, net)
        self.common_params = {"module": "transaction", "apikey": self.API_key}

    def get_contract_execution_status(self, txhash, **kwargs):
        params = {"action": "getstatus", "txhash": txhash}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None

    def get_transaction_receipt_status(self, txhash, **kwargs):
        params = {"action": "gettxreceiptstatus", "txhash": txhash}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        if r:
            return "success" if r.json()["result"]["status"] == "0" else "fail"
        return None

if __name__ == "__main__":
    api = EtherscanTransaction("key.json", "kovan")
    print(api.get_contract_execution_status("0x1353c25e9bdb298aea2f4e21418c9dfa652b893c3d1942cd43f265939cd6a176"))
