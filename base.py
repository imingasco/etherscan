from typing import *
import requests


class API:
    def __init__(self):
        self.session = requests.Session()

    def get(self, url: str, params: dict={}, **kwargs) -> requests.Response:
        param_str = "&".join([f"{k}={v}" for k, v in params.items()])
        url = (url + "?" + param_str).strip("?")
        r = self.session.get(url, **kwargs)
        return r

    def post(self, url: str, params: dict={}, **kwargs) -> requests.Response:
        r = self.session.post(url, data=params, **kwargs)
        return r
    
    def add_header(self, key: str, value) -> None:
        self.session.headers.update({key: value})
    
    def remove_header(self, key: str) -> None:
        self.session.headers.pop(key, None)
    
    def add_cookies(self, key: str, value, **kwargs) -> None:
        self.session.cookies.set(key, value, **kwargs)
    
    def delete_cookies(self, key: str) -> None:
        del self.session.cookies[key]

if __name__ == "__main__":
    api = API()
    
