from ast import Not
from etherscan import EtherscanAPI


class EtherscanBlock(EtherscanAPI):
    def __init__(self, file, net="mainnet"):
        super().__init__(file, net)
        self.common_params = {"module": "block", "apikey": self.API_key}

    def get_block_reward_and_uncle(self, block_number, **kwargs):
        params = {"action": "getblockreward", "blockno": block_number}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return (r.json()["result"]["blockReward"], r.json()["result"]["uncles"]) if r else None

    def get_estimated_block_countdown_time(self, block_number, **kwargs):
        params = {"action": "getblockcountdown", "blockno": block_number}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"]["EstimateTimeInSec"] if r else None
    
    def get_block_number_by_timestamp(self, timestamp, closest="before", **kwargs):
        params = {"action": "getblocknobytime", "timestamp": timestamp, "closest": closest}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None

    def get_daily_average_block_size(self, startdate, enddate, **kwargs):
        raise NotImplementedError("This api requires PRO!")

    def get_daily_block_count_and_reward(self, startdate, enddate, **kwargs):
        raise NotImplementedError("This api requires PRO!")

    def get_daily_block_rewards(self, startdate, enddate, **kwargs):
        raise NotImplementedError("This api requires PRO!")

    def get_daily_average_time_to_include_a_block(self, startdate, enddate, **kwargs):
        raise NotImplementedError("This api requires PRO!")

    def get_daily_uncle_block_count_and_rewards(self, startdate, enddate, **kwargs):
        raise NotImplementedError("This api requires PRO!")

if __name__ == "__main__":
    api = EtherscanBlock("key.json", "kovan")
    print(api.get_block_reward_and_uncle(30656000)[0])
