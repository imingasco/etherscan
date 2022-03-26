from etherscan import EtherscanAPI


class EtherscanProxy(EtherscanAPI):
    def __init__(self, file, net="mainnet"):
        super().__init__(file, net)
        self.common_params = {"module": "proxy", "apikey": self.API_key}
    
    def get_most_recent_block_number(self, **kwargs):
        params = {"action": "eth_blockNumber"}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None

    def get_block_information(self, block_number, boolean=True, **kwargs):
        params = {"action": "eth_getBlockByNumber", "tag": hex(block_number), "boolean": True}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None

    def get_uncle_block_by_number_and_index(self, block_number, index, **kwargs):
        params = {"action": "eth_getUncleByBlockNumberAndIndex", "tag": hex(block_number), "index": hex(index)}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None
    
    def get_block_transaction_count(self, block_number, **kwargs):
        params = {"action": "eth_getBlockTransactionCountByNumber", "tag": hex(block_number)}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return int(r.json()["result"], 16) if r else None
    
    def get_transaction_by_hash(self, txhash, **kwargs):
        params = {"action": "eth_getTransactionByHash", "txhash": txhash}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None

    def get_transaction_by_number_and_index(self, transaction_number, transaction_index, **kwargs):
        params = {"action": "eth_getTransactionByNumberAndIndex", "tag": hex(transaction_number), "index": hex(transaction_index)}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None

    def get_transaction_count_by_address(self, address, tag="latest", **kwargs):
        params = {"action": "eth_getTransactionCount", "address": address, "tag": tag}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return int(r.json()["result"], 16) if r else None

    def send_raw_transaction(self, raw, **kwargs):
        params = {"action": "eth_sendRawTransaction", "hex": raw}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None

    def get_transaction_receipt(self, txhash, **kwargs):
        params = {"action": "eth_getTransactionReceipt", "txhash": txhash}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None
    
    def message_call(self, dest, data, tag="latest", **kwargs):
        params = {"action": "eth_call", "to": dest, "data": data, "tag": tag}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None

    def get_code(self, address, tag="latest", **kwargs):
        params = {"action": "eth_call", "address": address, "tag": tag}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None

    def get_storage(self, address, position, tag, **kwargs):
        raise NotImplementedError("This api is still experimental, with potential danger")

    def get_gas_price_wei(self, **kwargs):
        params = {"action": "eth_gasPrice"}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return int(r.json()["result"], 16) if r else None
    
    def estimate_gas(self, data, dest, value, gas, gasPrice, **kwargs):
        params = {"action": "eth_estimateGas", "data": data, "to": dest, "value": hex(value), "gas": hex(gas), "gasPrice": hex(gasPrice)}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return int(r.json()["result"], 16) if r else None

if __name__ == "__main__":
    api = EtherscanProxy("key.json")
    print(api.get_block_information(0x10d4f))
