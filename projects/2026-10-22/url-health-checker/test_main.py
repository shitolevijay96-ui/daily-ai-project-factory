import pytest
from main import check_url, check_all

def and_mock_urlopen(monkeypatch, status_code):
    class MockResponse:
        status = status_code
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    monkeypatch.setattr("urllib.request.urlopen", lambda *args, **kwargs: MockResponse())

def test_check_url_success(monkeypatch):
    and_mock_urlopen(monkeypatch, 200)
    res = check_url("https://example.com")
    assert res["ok"] is True
    assert res["status"] == 200

def test_check_all():
    results = check_all(["https://httpbin.org/status/200"])
    assert isinstance(results, list)
    assert len(results) == 1
