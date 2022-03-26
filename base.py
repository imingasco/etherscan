from collections import deque
from typing import *
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.h3.connection import H3_ALPN, H3Connection
from aioquic.asyncio.client import connect
from urllib.parse import urlparse
import asyncio

def parse_url_port(url):
    _url = url.strip("https://")
    if len(_url.split(":", 1)) == 1:
        return url, 443
    else:
        return "https://" + _url.split(":")[0], _url.split(":")[1]


class HTTPClient(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._http = H3Connection(self._quic)
        self._request_events = {}
        self._request_waiter = {}
    
    def parse_basic_headers_from_url(self, url: str) -> list:
        parsed_result: dict(str, str) = urlparse(url)
        return [
            (b":method", b"GET"),
            (b":scheme", parsed_result["scheme"].encode()),
            (b":authority", parsed_result["netloc"].encode()),
            (b":path", parsed_result["path"].encode()),
            (b"user-agent", b"aioquic"),
        ]
        
    
    async def get(self, url: str, additional_headers: Optional[Dict]=None):
        basic_headers = self.parse_basic_headers_from_url(url)
        headers = basic_headers + [(k.encode(), v.encode()) for k, v in additional_headers.items()] if additional_headers else basic_headers
        stream_id = self._quic.get_next_available_stream_id()
        self._http.send_headers(
            stream_id=stream_id,
            headers=headers,
            end_stream=True,
        )
        waiter = self._loop.create_future()
        self._request_events[stream_id] = deque()
        self._request_waiter[stream_id] = waiter
        self.transmit()
        
        return await asyncio.shield(waiter)

class API:
    def __init__(self):
        self.configuration = QuicConfiguration(
            is_client=True, alpn_protocols=H3_ALPN
        )

    async def get(self, url: str, params: dict={}, **kwargs):
        param_str = "&".join([f"{k}={v}" for k, v in params.items()])
        url, port = parse_url_port(url)
        print(url, port)
        async with connect(url, port, configuration=self.configuration, create_protocol=HTTPClient) as client:
            r = await client.get(url + "?" + param_str, **kwargs)
            print(r)
            return r

if __name__ == "__main__":
    api = API()
    print(len("https://api-kovan.etherscan.io/api?action=balance&address=0x1a96b417224F4bEf2C4708f04fa801Af9fAc6D45&tag=latest&module=account&apikey=3W23CT4TXZEUR8ZA2ZCSG36GI4EQQA7NQD"))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(api.get("https://api-kovan.etherscan.io/api?action=balance"))
    
