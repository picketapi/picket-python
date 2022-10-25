from picketapi import types


def test_nonce_response():
    assert types.NonceResponse is not None

    nonce = "nonce"
    statement = "statement"
    format = "format"

    nonce_response = types.NonceResponse(nonce, statement, format)
    assert nonce_response is not None
    assert nonce_response.nonce == nonce
    assert nonce_response.statement == statement
    assert nonce_response.format == format

    # Test from_dict
    nonce_response_dict = {
        "nonce": nonce,
        "statement": statement,
        "format": format,
    }
    nonce_response = types.NonceResponse.from_dict(nonce_response_dict)
    assert nonce_response is not None
    assert nonce_response.nonce == nonce
    assert nonce_response.statement == statement
    assert nonce_response.format == format


def test_authorized_user():
    assert types.AuthorizedUser is not None

    chain = "chain"
    wallet_address = "wallet_address"
    display_address = "display_address"
    token_balances = {"contract_address": {"balance": "balance"}}

    authorized_user = types.AuthorizedUser(
        chain, wallet_address, display_address, token_balances
    )
    assert authorized_user is not None
    assert authorized_user.chain == chain
    assert authorized_user.wallet_address == wallet_address
    assert authorized_user.display_address == display_address
    assert authorized_user.token_balances == token_balances

    # Test from_dict
    authorized_user_dict = {
        "chain": chain,
        "walletAddress": wallet_address,
        "displayAddress": display_address,
        "tokenBalances": token_balances,
    }
    authorized_user = types.AuthorizedUser.from_dict(authorized_user_dict)
    assert authorized_user is not None
    assert authorized_user.chain == chain
    assert authorized_user.wallet_address == wallet_address
    assert authorized_user.display_address == display_address
    assert authorized_user.token_balances == token_balances


def test_auth_response():
    assert types.AuthResponse is not None

    access_token = "access_token"
    chain = "chain"
    wallet_address = "wallet_address"
    display_address = "display_address"
    token_balances = {"contract_address": {"balance": "balance"}}

    user = types.AuthorizedUser(chain, wallet_address, display_address, token_balances)
    auth_response = types.AuthResponse(access_token, user)
    assert auth_response is not None
    assert auth_response.access_token == access_token
    assert auth_response.user == user

    # Test from_dict
    auth_response_dict = {
        "accessToken": access_token,
        "user": {
            "chain": chain,
            "walletAddress": wallet_address,
            "displayAddress": display_address,
            "tokenBalances": token_balances,
        },
    }
    auth_response = types.AuthResponse.from_dict(auth_response_dict)
    assert auth_response is not None
    assert auth_response.access_token == access_token
    assert auth_response.user == user


def test_token_ownership_response():
    assert types.TokenOwnershipResponse is not None

    allowed = True
    token_balances = {"contractAddress": {"balance": "balance"}}

    token_ownership_response = types.TokenOwnershipResponse(allowed, token_balances)
    assert token_ownership_response is not None
    assert token_ownership_response.allowed == allowed
    assert token_ownership_response.token_balances == token_balances

    # Test from_dict
    token_ownership_response_dict = {
        "allowed": allowed,
        "tokenBalances": token_balances,
    }
    token_ownership_response = types.TokenOwnershipResponse.from_dict(
        token_ownership_response_dict
    )
    assert token_ownership_response is not None
    assert token_ownership_response.allowed == allowed
    assert token_ownership_response.token_balances == token_balances
