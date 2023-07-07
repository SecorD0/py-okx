from typing import Optional

import requests


class OKXAPIException(Exception):
    """
    An exception that occurs when the API is accessed unsuccessfully.

    Attributes:
        response (Optional[requests.Response]): an instance of a response to a request.
        code (int): an OKX error code.
        msg (str): an OKX error message.

    Args:
        response (Optional[requests.Response]): an instance of a response to a request. (None)

    """
    response: Optional[requests.Response]
    code: int
    msg: str

    def __init__(self, response: Optional[requests.Response] = None) -> None:
        self.response = response
        try:
            json_dict = response.json()
            self.code = json_dict.get('code')
            self.msg = json_dict.get('msg')

        except:
            pass

    def __str__(self) -> str:
        if self.code:
            return f'{self.code}, {self.msg}'

        return f'{self.response.status_code} (HTTP)'
