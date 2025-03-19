import pytest

from ..config import ET_ROOT
from ..client import _etrequest, get_project, check_available_version


def check_cxn(scope="session"):
    import requests

    try:
        requests.get("http://example.com")
        return True
    except Exception:
        return False


no_cxn = check_cxn() is False


@pytest.mark.skipif(no_cxn, reason="No connection")
def test_etrequest():
    endpoint = "http://fakeendpoint/"
    with pytest.raises(RuntimeError):
        _etrequest(endpoint, method="get")
    assert _etrequest(ET_ROOT)
    # ensure timeout is working properly
    endpoint = "https://google.com"
    with pytest.raises(RuntimeError):
        _etrequest(endpoint, timeout=0.001)
    assert _etrequest(endpoint)


@pytest.mark.skipif(no_cxn, reason="No connection")
def test_get_project():
    repo = "invalidrepo"
    with pytest.raises(ValueError):
        get_project(repo)
    repo = "github/hub"
    res = get_project(repo)
    assert "version" in res


def test_noet():
    import os

    old_var = None
    if "NO_ET" in os.environ:
        old_var = (True, os.environ["NO_ET"])
    os.environ["NO_ET"] = "1"
    repo = "github/hub"
    res = get_project(repo)
    assert res is None
    if old_var is None:
        del os.environ["NO_ET"]
    else:
        os.environ["NO_ET"] = old_var[1]


@pytest.mark.skipif(no_cxn, reason="No connection")
def test_check_available():
    repo = "invalidrepo"
    res = check_available_version(repo, "0.1.0")
    assert res is None
    repo = "github/hub"
    res = check_available_version(repo, "0.1.0")
    assert "version" in res
    res = check_available_version(repo, res["version"])
    assert "version" in res
    res = check_available_version(repo, "1000.1.0")
    assert "version" in res
