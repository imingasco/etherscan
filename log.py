from etherscan import EtherscanAPI


class EtherscanLog(EtherscanAPI):
    def __init__(self, file, net="mainnet"):
        super().__init__(file, net)
        self.common_params = {"module": "log", "apikey": self.API_key}

    def get_log(self, from_block="379224", to_block="latest", **kwargs):
        options = ["address", "topic0", "topic1", "topic2", "topic3", "topic0_1_opr", "topic0_2_opr", "topic0_3_opr", "topic1_2_opr", "topic1_3_opr", "topic2_3_opr"]
        params = {"action": "getLogs", "fromBlock": from_block, "to_block": to_block}
        for k, v in kwargs.items():
            if k in options:
                kwargs.pop(k)
                params[k] = v
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None

    def get_log_with_specific_block_range(self, from_block, to_block, **kwargs):
        return self.get_log(from_block=from_block, to_block=to_block, **kwargs)
    
    def get_log_with_specific_log_address(self, from_block, to_block, address, **kwargs):
        return self.get_log(from_block=from_block, to_block=to_block, address=address, **kwargs)
    
    def get_log_with_specific_topic0(self, from_block, to_block, topic0, **kwargs):
        return self.get_log(from_block=from_block, to_block=to_block, topic0=topic0, **kwargs)

    def get_log_with_specific_topic1(self, from_block, to_block, topic1, **kwargs):
        return self.get_log(from_block=from_block, to_block=to_block, topic1=topic1, **kwargs)

    def get_log_with_specific_topic2(self, from_block, to_block, topic2, **kwargs):
        return self.get_log(from_block=from_block, to_block=to_block, topic2=topic2, **kwargs)

    def get_log_with_specific_topic3(self, from_block, to_block, topic3, **kwargs):
        return self.get_log(from_block=from_block, to_block=to_block, topic3=topic3, **kwargs)

    def get_log_with_specific_topic0_topic1(self, from_block, to_block, topic0, topic1, topic0_1_opr, **kwargs):
        return self.get_log(from_block=from_block, to_block=to_block, topic0=topic0, topic1=topic1, topic0_1_opr=topic0_1_opr, **kwargs)

    def get_log_with_specific_topic0_topic2(self, from_block, to_block, topic0, topic2, topic0_2_opr, **kwargs):
        return self.get_log(from_block=from_block, to_block=to_block, topic0=topic0, topic2=topic2, topic0_2_opr=topic0_2_opr, **kwargs)
    
    def get_log_with_specific_topic0_topic3(self, from_block, to_block, topic0, topic3, topic0_3_opr, **kwargs):
        return self.get_log(from_block=from_block, to_block=to_block, topic0=topic0, topic3=topic3, topic0_3_opr=topic0_3_opr, **kwargs)
    
    def get_log_with_specific_topic1_topic2(self, from_block, to_block, topic1, topic2, topic1_2_opr, **kwargs):
        return self.get_log(from_block=from_block, to_block=to_block, topic1=topic1, topic2=topic2, topic1_2_opr=topic1_2_opr, **kwargs)
    
    def get_log_with_specific_topic1_topic3(self, from_block, to_block, topic1, topic3, topic1_3_opr, **kwargs):
        return self.get_log(from_block=from_block, to_block=to_block, topic1=topic1, topic3=topic3, topic1_3_opr=topic1_3_opr, **kwargs)

    def get_log_with_specific_topic2_topic3(self, from_block, to_block, topic2, topic3, topic2_3_opr, **kwargs):
        return self.get_log(from_block=from_block, to_block=to_block, topic2=topic2, topic3=topic3, topic2_3_opr=topic2_3_opr, **kwargs)
