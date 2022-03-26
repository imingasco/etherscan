from typing import *
import requests
import http3


class API:
    def __init__(self):
        self.headers = {}
        self.cookies = {}

    def get(self, url: str, params: dict={}, **kwargs) -> requests.Response:
        param_str = "&".join([f"{k}={v}" for k, v in params.items()])
        url = (url + "?" + param_str).strip("?")
        r = http3.get(url, headers=self.headers, cookies=self.cookies, **kwargs)
        return r

    def post(self, url: str, params: dict={}, **kwargs) -> requests.Response:
        r = http3.post(url, headers=self.headers, cookies=self.cookies, data=params, **kwargs)
        return r

    def add_header(self, key, value):
        self.headers[key] = value
    
    def remove_header(self, key):
        self.headers.pop(key, None)
    
    def add_cookies(self, key, value):
        self.cookies[key] = value

    def remove_cookies(self, key):
        self.cookies.pop(key, None)
    
if __name__ == "__main__":
    api = API()
    
