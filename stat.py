from etherscan import EtherscanAPI


class EtherscanStat(EtherscanAPI):
    def __init__(self, file, net="mainnet"):
        super().__init__(file, net)
        self.common_params = {"module": "stats", "apikey": self.API_key}

    def get_ether_total_supply(self, **kwargs):
        params = {"action": "ethsupply"}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return int(r.json()["result"]) if r else None

    def get_ether_2_total_supply(self, **kwargs):
        params = {"action": "ethsupply2"}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return int(r.json()["result"]) if r else None

    def get_last_ether_price(self, **kwargs):
        params = {"action": "ethprice"}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None

    def get_chain_size_within_date(self, startdate, enddate, clienttype="geth", syncmode="default", sort="asc", **kwargs):
        params = {"action": "chainsize", "startdate": startdate, "enddate": enddate, "clienttype": clienttype, "syncmode": syncmode, "sort": sort}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return r.json()["result"] if r else None

    def get_number_of_nodes(self, **kwargs):
        params = {"action": "nodecount"}
        params.update(self.common_params)
        r = self.get(params, **kwargs)
        return int(r.json()["result"]["TotalNodeCount"]) if r else None

    def get_daily_transaction_fee(self, startdate, enddate, sort="asc", **kwargs):
        raise NotImplementedError("This api requires PRO!")

    def get_number_of_daily_new_address(self, startdate, enddate, sort="asc", **kwargs):
        raise NotImplementedError("This api requires PRO!")

    def get_daily_utilization(self, startdate, enddate, sort="asc", **kwargs):
        raise NotImplementedError("This api requires PRO!")

    def get_daily_average_hash_rate(self, startdate, enddate, sort="asc", **kwargs):
        raise NotImplementedError("This api requires PRO!")

    def get_daily_transaction_count(self, startdate, enddate, sort="asc", **kwargs):
        raise NotImplementedError("This api requires PRO!")

    def get_daily_average_difficulty(self, startdate, enddate, sort="asc", **kwargs):
        raise NotImplementedError("This api requires PRO!")

    def get_ether_historical_daily_market_cap(self, startdate, enddate, sort="asc", **kwargs):
        raise NotImplementedError("This api requires PRO!")

    def get_ether_historical_price(self, startdate, enddate, sort="asc", **kwargs):
        raise NotImplementedError("This api requires PRO!")

if __name__ == "__main__":
    api = EtherscanStat("key.json", "kovan")
    print(api.get_ether_total_supply())
