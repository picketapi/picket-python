import os

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import JSONDecodeError

from .exceptions import PicketAPIException
from .helpers import is_successful_status_code, snake_to_camel_keys
from .types import (
    NonceResponse,
    AuthorizedUser,
    AuthResponse,
    TokenOwnershipResponse,
)

API_VERSION = "v1"
API_BASE_URL = os.path.join("https://picketapi.com/api/", API_VERSION)


class Picket:
    def __init__(self, api_key: str, **kwargs):
        self.api_key = api_key
        # Base URL for API
        # Configurable for testing
        self.base_url = kwargs.get("base_url", API_BASE_URL)

    def headers(self):
        return {
            "User-Agent": "Picket Python Client",
            "Content-Type": "application/json",
        }

    def post_request(self, path: str, **kwargs):
        url = os.path.join(self.base_url, path)
        auth = HTTPBasicAuth(self.api_key, "")
        headers = self.headers()

        # transform keys to camelCase
        req = requests.post(
            url, auth=auth, headers=headers, json=snake_to_camel_keys(kwargs)
        )
        try:
            data = req.json()
        except JSONDecodeError:
            raise Exception(req.text)

        if not is_successful_status_code(req.status_code):
            if "msg" not in data:
                raise Exception(data)
            # msg is required, code is optional
            raise PicketAPIException(data["msg"], data.get("code", None))

        return data

    # nonce
    def nonce(
        self, chain: str, wallet_address: str, locale: str = "en-US"
    ) -> NonceResponse:
        data = self.post_request(
            "auth/nonce", chain=chain, wallet_address=wallet_address, locale=locale
        )
        return NonceResponse.from_dict(data)

    def auth(
        self,
        chain: str,
        wallet_address: str,
        signature: str,
        requirements: dict = {},
        context: dict = {},
    ) -> AuthResponse:
        data = self.post_request(
            "auth",
            chain=chain,
            wallet_address=wallet_address,
            signature=signature,
            requirements=requirements,
            context=context,
        )
        return AuthResponse.from_dict(data)

    def authz(
        self, access_token: str, requirements: dict, revalidate: bool = False
    ) -> AuthResponse:
        data = self.post_request(
            "authz",
            access_token=access_token,
            requirements=requirements,
            revalidate=revalidate,
        )
        return AuthResponse.from_dict(data)

    def validate(self, access_token: str, requirements: dict = {}) -> AuthorizedUser:
        data = self.post_request(
            "auth/validate", access_token=access_token, requirements=requirements
        )
        return AuthorizedUser.from_dict(data)

    def token_ownesrhip(
        self, chain: str, wallet_address: str, **kwargs
    ) -> TokenOwnershipResponse:
        path = os.path.join(
            "chains", chain, "wallets", wallet_address, "tokenOwnership"
        )
        data = self.post_request(path, **kwargs)
        return TokenOwnershipResponse.from_dict(data)
