# picket-python

The official Python library for the [Picket API](https://picketapi.com/)

## Installation

```bash 
pip install -U picketapi
```

## Usage - Quick Start

Use the `Picket` class to create the Picket API client. It takes a _secret API key_ as a parameter.

```python
from picketapi import Picket

picket = new Picket("YOU_SECRET_API_KEY")
```

## Nonce

A `nonce` is random value generated by the Picket API to that user must sign to prove ownership a wallet address. The `nonce` function can be used to implement your own wallet authentication flow. 

A nonce is unique to a project and wallet address. If a `nonce` doesn't exist for the project and wallet address, Picket will generate a new nonce; otherwise, Picket will return the existing nonce. A nonce is valid for two minutes before self-destructing.

```python
resp = picket.nonce(chain="solana", wallet_address="wAlLetTAdDress")
# resp is of type NonceResponse
print(resp.nonce)
```

## Auth

`auth` is the server-side equivalent of login. `auth` should only be used in a trusted server environment. The most common use-case for `auth` is [linking a wallet to an existing application account](https://docs.picketapi.com/picket-docs/tutorials/link-a-wallet-to-a-web-2.0-account).

```python
resp = picket.auth(chain="ethereum", wallet_address="0x1234567890", signature="abcdefghijklmnop")
# resp is of type AuthResponse
print(resp.user)
print(resp.access_token)
```

## Authz (Authorize)
`authz` stands for authorization. Unlike Auth, which handles both authentication and authorization, Authz only handles authorization. 
Given an authenticated user's access token and authorization requirements, `authz` will issue a new access token on success (user is authorized) or, on failure, it will return a 4xx HTTP error code.

```python
resp = picket.authz(access_token="xxx.yyy.zzz", requirements={ "contractAddress": "0xContract" })
# resp is of type AuthResponse
print(resp.user)
print(resp.access_token)
```

## Validate
`validate` validates an access token. `validate` should be called, or manually access token validation should be done, server-side before trusting a request's access token. It's common to move access token validation and decoding logic to a shared middleware across API endpoints.
If the access token is valid, validate returns the decoded claims of the access token.

```python
resp, err := picket.validate(access_token="xxx.yyy.zzz", requirements={"contractAddress": "0xContract", "minTokenBalance": "100"})
# Response is the decoded access token (AuthorizedUser)
print(resp)
```

## Verify Token Ownership
If you only want to verify token ownership server side for a given wallet, `tokenOwnership` allows you to do just that.

```python
resp = picket.token_ownership(
			chain="solana", 
			wallet_address="waLLETaddRess", 
			requirements={  
			  "collection": "METAPLEX_COLLECTION",
			  "minTokenBalance": "3",
			}
		)
# Response is of type TokenOwnershipResponse
print(resp.allowed)
print(resp.tokenBalances)
```

