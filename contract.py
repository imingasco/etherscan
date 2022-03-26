from etherscan import EtherscanAPI


class EtherscanContract(EtherscanAPI):
    def __init__(self, file, net="mainnet"):
        super().__init__(file, net)
        self.common_params = {"module": "contract", "apikey": self.API_key}

    def get_ABI_of_verified_contract(self, address, **kwargs):
        params = {"action": "getabi", "address": address}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None

    def get_source_of_verified_contract(self, address, **kwargs):
        params = {"action": "getsourcecode", "address": address}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"][0]["SourceCode"] if r else None

    def verify_source_code(self, contract_address, code, **kwargs):
        raise NotImplementedError("Implement later")

    def get_source_code_verification_status(self, guid, **kwargs):
        raise NotImplementedError("Implement later")

    def verify_proxy_contract(self, address, **kwargs):
        raise NotImplementedError("Implement later")

    def get_proxy_contract_verification_status(self, guid, **kwargs):
        raise NotImplementedError("Implement later")

if __name__ == "__main__":
    api = EtherscanContract("key.json", "mainnet")
    print(api.get_source_of_verified_contract("0xBB9bc244D798123fDe783fCc1C72d3Bb8C189413"))
