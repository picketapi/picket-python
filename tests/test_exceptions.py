from picketapi import exceptions


def test_picket_api_exception():
    assert exceptions.PicketAPIException is not None


def test_picket_api_exception_init():
    msg = "msg"
    code = "code"
    exception = exceptions.PicketAPIException(msg, code)
    assert exception.msg == msg
    assert exception.code == code


def test_picket_api_exception_str():
    msg = "msg"
    code = "code"
    exception = exceptions.PicketAPIException(msg, code)
    assert str(exception) == msg
