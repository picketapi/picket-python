from dataclasses import dataclass
from typing import Dict


@dataclass
class NonceResponse:
    nonce: str
    statement: str
    format: str

    @classmethod
    def from_dict(cls, d):
        return cls(d["nonce"], d["statement"], d["format"])


TokenBalances = Dict[str, Dict[str, str]]


@dataclass
class AuthorizedUser:
    chain: str
    wallet_address: str
    display_address: str
    token_balances: TokenBalances

    @classmethod
    def from_dict(cls, d):
        return cls(
            d["chain"], d["walletAddress"], d["displayAddress"], d["tokenBalances"]
        )


@dataclass
class AuthResponse:
    access_token: str
    user: AuthorizedUser

    @classmethod
    def from_dict(cls, d):
        user = AuthorizedUser.from_dict(d["user"])
        return cls(d["accessToken"], user)


@dataclass
class TokenOwnershipResponse:
    allowed: bool
    token_balances: TokenBalances

    @classmethod
    def from_dict(cls, d):
        return cls(d["allowed"], d["tokenBalances"])
