import pytest

def hello():
    return 'hello'

def test_says_hello():
    assert hello() == 'hello'
