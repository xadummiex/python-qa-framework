from typing import Callable

import requests

from src.api.endpoint import Endpoint
from src.config import settings


class HttpRequester:
    def __init__(self, session: requests.Session, endpoint: Endpoint,
                 http_check: Callable, base_url: str = settings.base_url):
        self.session = session
        self.endpoint = endpoint
        self.http_check = http_check
        self.base_url = base_url
