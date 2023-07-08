import base64
import hmac
import json
from datetime import datetime
from typing import Optional, Union, Dict, Any
from urllib.parse import urlencode

import requests

from py_okx import exceptions
from py_okx.models import OKXCredentials, Methods


class Base:
    """
    The base class for all section classes.

    Attributes:
        entrypoint_url (str): an entrypoint URL.
        proxy (Dict[str, str]): an HTTP or SOCKS5 IPv4 proxy dictionary.

    """
    __credentials: OKXCredentials
    entrypoint_url: str
    proxy: Optional[Dict[str, str]]

    def __init__(self, credentials: OKXCredentials, entrypoint_url: str, proxy: Optional[str]) -> None:
        """
        Initialize the class.

        Args:
            credentials (OKXCredentials): an instance with all OKX API key data.
            entrypoint_url (str): an API entrypoint url.
            proxy (Optional[str]): an HTTP or SOCKS5 IPv4 proxy in one of the following formats:
                - login:password@proxy:port
                - http://login:password@proxy:port
                - socks5://login:password@proxy:port
                - proxy:port
                - http://proxy:port

        """
        self.__credentials = credentials
        self.entrypoint_url = entrypoint_url
        self.proxy = proxy

    @staticmethod
    def get_timestamp() -> str:
        """
        Get the current timestamp.

        Returns:
            str: the current timestamp.

        """
        return datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'

    def generate_sign(self, timestamp: str, method: str, request_path: str, body: Union[dict, str]) -> bytes:
        """
        Generate signed message.

        Args:
            timestamp (str): the current timestamp.
            method (str): the request method is either GET or POST.
            request_path (str): the path of requesting an endpoint.
            body (Union[dict, str]): POST request parameters.

        Returns:
            bytes: the signed message.

        """
        if not body:
            body = ''

        if isinstance(body, dict):
            body = json.dumps(body)

        key = bytes(self.__credentials.secret_key, encoding='utf-8')
        msg = bytes(timestamp + method + request_path + body, encoding='utf-8')
        return base64.b64encode(hmac.new(key, msg, digestmod='sha256').digest())

    def make_request(
            self, method: str, request_path: str, body: Optional[dict] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Make a request to the OKX API.

        Args:
            method (str): the request method is either GET or POST.
            request_path (str): the path of requesting an endpoint.
            body (Optional[dict]): request parameters. (None)

        Returns:
            Optional[Dict[str, Any]]: the request response.

        """
        timestamp = self.get_timestamp()
        method = method.upper()
        body = body if body else {}
        if method == Methods.GET and body:
            request_path += f'?{urlencode(query=body)}'
            body = {}

        sign_msg = self.generate_sign(timestamp=timestamp, method=method, request_path=request_path, body=body)
        url = self.entrypoint_url + request_path
        header = {
            'Content-Type': 'application/json',
            'OK-ACCESS-KEY': self.__credentials.api_key,
            'OK-ACCESS-SIGN': sign_msg.decode(),
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.__credentials.passphrase
        }
        if method == Methods.POST:
            response = requests.post(
                url, headers=header, proxies=self.proxy, data=json.dumps(body) if isinstance(body, dict) else body
            )

        else:
            response = requests.get(url, headers=header, proxies=self.proxy, timeout=30)

        json_response = response.json()
        if int(json_response.get('code')):
            raise exceptions.APIException(response=response)

        return json_response
