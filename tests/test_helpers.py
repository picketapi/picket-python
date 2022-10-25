from picketapi import helpers


def test_is_successful_status_code_true():
    assert helpers.is_successful_status_code(201) is True


def test_is_successful_status_code_false():
    assert helpers.is_successful_status_code(400) is False


def test_snake_to_camel():
    assert helpers.snake_to_camel("snake_to_camel") == "snakeToCamel"
    assert helpers.snake_to_camel("wallet_address") == "walletAddress"
    assert helpers.snake_to_camel("contractAddress") == "contractAddress"
    assert helpers.snake_to_camel("token_ids") == "tokenIds"


def test_snake_to_camel_keys():
    d = {"snake_to_camel": "snake_to_camel", "wallet_address": "wallet_address"}
    assert helpers.snake_to_camel_keys(d) == {
        "snakeToCamel": "snake_to_camel",
        "walletAddress": "wallet_address",
    }


def test_snake_to_camel_keys_nested():
    d = {
        "snake_to_camel": "snake_to_camel",
        "walletAddress": "wallet_address",
        "nested": {
            "nest_one": "value",
            "nest_two": {
                "nest_three": "value",
            },
        },
    }
    assert helpers.snake_to_camel_keys(d) == {
        "snakeToCamel": "snake_to_camel",
        "walletAddress": "wallet_address",
        "nested": {
            "nestOne": "value",
            "nestTwo": {
                "nestThree": "value",
            },
        },
    }
