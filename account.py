from etherscan import EtherscanAPI


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
    api = EtherscanAccount("key.json", "kovan")
    print(api.get_address_balance("0x1a96b417224F4bEf2C4708f04fa801Af9fAc6D45"))
