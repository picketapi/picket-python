import base64
import os
import pytest
import responses
from responses import matchers

from picketapi import Picket
from picketapi import types
from picketapi.exceptions import PicketAPIException
from picketapi.helpers import snake_to_camel_keys


def test_picket():
    assert Picket is not None


def test_picket_init():
    api_key = "api_key"
    picket = Picket(api_key)
    assert picket is not None
    assert picket.api_key == api_key


@pytest.fixture
def picket():
    return Picket("api_key")


def test_picket_headers(picket):
    headers = picket.headers()
    assert headers == {
        "User-Agent": "Picket Python Client",
        "Content-Type": "application/json",
    }


@responses.activate
def test_picket_post_request(picket):
    method = "POST"
    path = "path"
    data = {"data": "data"}
    status = 200

    basic_auth = base64.b64encode(f"{picket.api_key}:".encode("utf-8")).decode("utf-8")

    # Register via 'Response' object
    mock = responses.Response(
        method=method,
        # Check url
        url=os.path.join(picket.base_url, path),
        content_type="application/json",
        status=status,
        json=data,
        match=[
            # Check data/body
            matchers.json_params_matcher(snake_to_camel_keys(data)),
            # Check headers
            matchers.header_matcher(picket.headers()),
            # Check auth
            matchers.header_matcher({"Authorization": f"Basic {basic_auth}"}),
        ],
    )
    responses.add(mock)

    resp = picket.post_request(path, **data)
    assert resp is not None
    assert resp == data


@responses.activate
def test_picket_nonce(picket):
    method = "POST"
    path = "auth/nonce"

    req_data = {
        "wallet_address": "wallet_address",
        "chain": "chain",
        "locale": "locale",
    }
    resp_data = {
        "nonce": "nonce",
        "statement": "statement",
        "format": "format",
    }
    status = 200

    basic_auth = base64.b64encode(f"{picket.api_key}:".encode("utf-8")).decode("utf-8")

    # Register via 'Response' object
    mock = responses.Response(
        method=method,
        # Check url
        url=os.path.join(picket.base_url, path),
        content_type="application/json",
        status=status,
        json=resp_data,
        match=[
            # Check data/body
            matchers.json_params_matcher(snake_to_camel_keys(req_data)),
            # Check headers
            matchers.header_matcher(picket.headers()),
            # Check auth
            matchers.header_matcher({"Authorization": f"Basic {basic_auth}"}),
        ],
    )
    responses.add(mock)

    resp = picket.nonce(**req_data)

    assert resp is not None
    assert type(resp) == types.NonceResponse
    assert resp.nonce == resp_data["nonce"]
    assert resp.statement == resp_data["statement"]
    assert resp.format == resp_data["format"]


@responses.activate
def test_picket_auth(picket):
    method = "POST"
    path = "auth"

    req_data = {
        "chain": "chain",
        "wallet_address": "wallet_address",
        "signature": "signature",
        "requirements": {"requirements": "requirements"},
        "context": {"context": "context"},
    }
    resp_data = {
        "user": {
            "chain": "chain",
            "walletAddress": "wallet_address",
            "displayAddress": "display_address",
            "tokenBalances": {
                "contractAddress": {
                    "0x12345": "1",
                },
            },
        },
        "accessToken": "xxx.yyy.zzz",
    }
    status = 200

    basic_auth = base64.b64encode(f"{picket.api_key}:".encode("utf-8")).decode("utf-8")

    # Register via 'Response' object
    mock = responses.Response(
        method=method,
        # Check url
        url=os.path.join(picket.base_url, path),
        content_type="application/json",
        status=status,
        json=resp_data,
        match=[
            # Check data/body
            matchers.json_params_matcher(snake_to_camel_keys(req_data)),
            # Check headers
            matchers.header_matcher(picket.headers()),
            # Check auth
            matchers.header_matcher({"Authorization": f"Basic {basic_auth}"}),
        ],
    )
    responses.add(mock)

    resp = picket.auth(**req_data)

    assert resp is not None
    assert type(resp) == types.AuthResponse
    assert resp.access_token == resp_data["accessToken"]
    assert type(resp.user) == types.AuthorizedUser

    user = resp.user
    assert user.chain == resp_data["user"]["chain"]
    assert user.wallet_address == resp_data["user"]["walletAddress"]
    assert user.token_balances == resp_data["user"]["tokenBalances"]


@responses.activate
def test_picket_authz(picket):
    method = "POST"
    path = "authz"

    req_data = {
        "access_token": "xxx.yyy.zzz",
        "requirements": {"requirements": "requirements"},
        "revalidate": True,
    }
    resp_data = {
        "user": {
            "chain": "chain",
            "walletAddress": "wallet_address",
            "displayAddress": "display_address",
            "tokenBalances": {
                "contractAddress": {
                    "0x12345": "1",
                },
            },
        },
        "accessToken": "aaa.bbb.ccc",
    }
    status = 200

    basic_auth = base64.b64encode(f"{picket.api_key}:".encode("utf-8")).decode("utf-8")

    # Register via 'Response' object
    mock = responses.Response(
        method=method,
        # Check url
        url=os.path.join(picket.base_url, path),
        content_type="application/json",
        status=status,
        json=resp_data,
        match=[
            # Check data/body
            matchers.json_params_matcher(snake_to_camel_keys(req_data)),
            # Check headers
            matchers.header_matcher(picket.headers()),
            # Check auth
            matchers.header_matcher({"Authorization": f"Basic {basic_auth}"}),
        ],
    )
    responses.add(mock)

    resp = picket.authz(**req_data)

    assert resp is not None
    assert type(resp) == types.AuthResponse
    assert resp.access_token == resp_data["accessToken"]
    assert type(resp.user) == types.AuthorizedUser

    user = resp.user
    assert user.chain == resp_data["user"]["chain"]
    assert user.wallet_address == resp_data["user"]["walletAddress"]
    assert user.token_balances == resp_data["user"]["tokenBalances"]


@responses.activate
def test_picket_validate(picket):
    method = "POST"
    path = "auth/validate"

    req_data = {
        "access_token": "xxx.yyy.zzz",
        "requirements": {"requirements": "requirements"},
    }
    resp_data = {
        "chain": "chain",
        "walletAddress": "wallet_address",
        "displayAddress": "display_address",
        "tokenBalances": {
            "contractAddress": {
                "0x12345": "1",
            },
        },
    }
    status = 200

    basic_auth = base64.b64encode(f"{picket.api_key}:".encode("utf-8")).decode("utf-8")

    # Register via 'Response' object
    mock = responses.Response(
        method=method,
        # Check url
        url=os.path.join(picket.base_url, path),
        content_type="application/json",
        status=status,
        json=resp_data,
        match=[
            # Check data/body
            matchers.json_params_matcher(snake_to_camel_keys(req_data)),
            # Check headers
            matchers.header_matcher(picket.headers()),
            # Check auth
            matchers.header_matcher({"Authorization": f"Basic {basic_auth}"}),
        ],
    )
    responses.add(mock)

    resp = picket.validate(**req_data)

    assert resp is not None
    assert type(resp) == types.AuthorizedUser
    assert resp.chain == resp_data["chain"]
    assert resp.wallet_address == resp_data["walletAddress"]
    assert resp.token_balances == resp_data["tokenBalances"]


@responses.activate
def test_picket_token_ownership(picket):
    method = "POST"
    chain = "chain"
    wallet_address = "wallet_address"

    req_data = {
        "token_ids": [1, 2, 3, 4, 5],
    }

    path = os.path.join(
        "chains",
        chain,
        "wallets",
        wallet_address,
        "tokenOwnership",
    )

    resp_data = {
        "allowed": False,
        "tokenBalances": {
            "token_ids": {
                "1": 1,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
            }
        },
    }

    status = 200

    basic_auth = base64.b64encode(f"{picket.api_key}:".encode("utf-8")).decode("utf-8")

    # Register via 'Response' object
    mock = responses.Response(
        method=method,
        # Check url
        url=os.path.join(picket.base_url, path),
        content_type="application/json",
        status=status,
        json=resp_data,
        match=[
            # Check data/body
            matchers.json_params_matcher(snake_to_camel_keys(req_data)),
            # Check headers
            matchers.header_matcher(picket.headers()),
            # Check auth
            matchers.header_matcher({"Authorization": f"Basic {basic_auth}"}),
        ],
    )
    responses.add(mock)

    resp = picket.token_ownesrhip(chain, wallet_address, **req_data)

    assert resp is not None
    assert type(resp) == types.TokenOwnershipResponse
    assert resp.allowed == resp_data["allowed"]
    assert resp.token_balances == resp_data["tokenBalances"]


# Test Picket error response
@responses.activate
def test_picket_error(picket):
    method = "POST"
    path = "authz"

    req_data = {
        "access_token": "xxx.yyy.zzz",
        "requirements": {"requirements": "requirements"},
        "revalidate": True,
    }
    resp_data = {
        "code": "code",
        "msg": "message",
    }
    status = 400

    basic_auth = base64.b64encode(f"{picket.api_key}:".encode("utf-8")).decode("utf-8")

    # Register via 'Response' object
    mock = responses.Response(
        method=method,
        # Check url
        url=os.path.join(picket.base_url, path),
        content_type="application/json",
        status=status,
        json=resp_data,
        match=[
            # Check data/body
            matchers.json_params_matcher(snake_to_camel_keys(req_data)),
            # Check headers
            matchers.header_matcher(picket.headers()),
            # Check auth
            matchers.header_matcher({"Authorization": f"Basic {basic_auth}"}),
        ],
    )
    responses.add(mock)

    with pytest.raises(PicketAPIException) as e:
        picket.authz(**req_data)

    assert e.value.msg == resp_data["msg"]
    assert e.value.code == resp_data["code"]


# Test unknown error response
@responses.activate
def test_picket_unknown_error(picket):
    method = "POST"
    path = "authz"

    req_data = {
        "access_token": "xxx.yyy.zzz",
        "requirements": {"requirements": "requirements"},
        "revalidate": True,
    }
    resp_data = "something went wrong."
    status = 500

    basic_auth = base64.b64encode(f"{picket.api_key}:".encode("utf-8")).decode("utf-8")

    # Register via 'Response' object
    mock = responses.Response(
        method=method,
        # Check url
        url=os.path.join(picket.base_url, path),
        content_type="application/json",
        status=status,
        json=resp_data,
        match=[
            # Check data/body
            matchers.json_params_matcher(snake_to_camel_keys(req_data)),
            # Check headers
            matchers.header_matcher(picket.headers()),
            # Check auth
            matchers.header_matcher({"Authorization": f"Basic {basic_auth}"}),
        ],
    )
    responses.add(mock)

    with pytest.raises(Exception) as e:
        picket.authz(**req_data)

    assert str(e.value) == resp_data
