import pytest
from pydantic import ValidationError

from app.schemas.chat import ChatRequest


def test_rejects_empty_message():
    with pytest.raises(ValidationError):
        ChatRequest(message="")


def test_rejects_whitespace_only_message():
    with pytest.raises(ValidationError):
        ChatRequest(message="   ")


def test_rejects_overlong_message():
    with pytest.raises(ValidationError):
        ChatRequest(message="x" * 2001)


def test_strips_surrounding_whitespace():
    request = ChatRequest(message="  hello  ")
    assert request.message == "hello"


def test_accepts_valid_message():
    request = ChatRequest(message="What is the leave policy?")
    assert request.session_id is None
