class PicketAPIException(Exception):
    def __init__(self, msg: str, code: str):
        super().__init__(msg)
        self.msg = msg
        self.code = code

    def __str__(self):
        return self.msg
