def is_successful_status_code(status_code: int) -> bool:
    return status_code >= 200 and status_code < 300


def snake_to_camel(name: str) -> str:
    parts = name.split("_")
    return "".join(word if idx == 0 else word.title() for idx, word in enumerate(parts))


def snake_to_camel_keys(d: dict) -> dict:
    return {
        snake_to_camel(k): v if type(v) is not dict else snake_to_camel_keys(v)
        for k, v in d.items()
    }
