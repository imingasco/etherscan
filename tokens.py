from etherscan import EtherscanAPI


class EtherscanToken(EtherscanAPI):
    def __init__(self, file, net="mainnet"):
        super().__init__(file, net)
        self.common_params = {"apikey": self.API_key}

    def get_erc20_token_total_supply_by_contract_address(self, contract_address, **kwargs):
        params = {"module": "stats", "action": "tokensupply", "contractaddress": contract_address}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return int(r.json()["result"]) if r else None

    def get_address_erc20_token_account_balance(self, address, contract_address, tag="latest", **kwargs):
        params = {"module": "account", "action": "tokenbalance", "contractaddress": contract_address, "address": address, "tag": tag}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return int(r.json()["result"]) if r else None

    def get_historical_erc20_token_total_supply_by_contract_address_and_block_number(self, contract_address, block_number, **kwargs):
        raise NotImplementedError("This api requires PRO!")

    def get_historical_erc20_token_account_balance_by_contract_address_and_block_number(self, contract_address, address, block_number, **kwargs):
        raise NotImplementedError("This api requires PRO!")
    
    def get_token_info(self, contract_address, **kwargs):
        raise NotImplementedError("This api requires PRO!")

if __name__ == "__main__":
    api = EtherscanToken("key.json")
    print(api.get_erc20_token_total_supply_by_contract_address("0x57d90b64a1a57749b0f932f1a3395792e12e7055"))