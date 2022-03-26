from ast import Not
from etherscan import EtherscanAPI


class EtherscanGasTracker(EtherscanAPI):
    def __init__(self, file, net="mainnet"):
        super().__init__(file, net)
        self.common_params = {"module": "gastracker", "apikey": self.API_key}

    def estimate_confirmation_time(self, gas_price, **kwargs):
        params = {"action": "gasestimate", "gasprice": gas_price}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return int(r.json()["result"]) if r else None

    def gas_oracle(self, **kwargs):
        params = {"action": "gasoracle"}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None

    def get_daily_average_gas_limit(self, startdate, enddate, sort="asc"):
        raise NotImplementedError("This api requires PRO!")

    def get_daily_total_used_gas(self, startdate, enddate, sort="asc"):
        raise NotImplementedError("This api requires PRO!")

    def get_daily_average_gas_price(self, startdate, enddate, sort="asc"):
        raise NotImplementedError("This api requires PRO!")

if __name__ == "__main__":
    api = EtherscanGasTracker("key.json", "kovan")
    print(api.estimate_confirmation_time(30000000000))