from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json

class Response:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self._data = data

    def json(self):
        return self._data

def get(url):
    req = Request(
        url,
        headers={"User-Agent": "python-cli"}
    )
    try:
        with urlopen(req, timeout=5) as response:
            data = json.load(response)
            status = response.getcode()
    except HTTPError as e:
        status = e.code
        data = {}

    return Response(status, data)



