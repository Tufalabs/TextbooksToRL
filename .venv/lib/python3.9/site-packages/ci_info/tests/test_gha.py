"""Test should only pass in Github Actions environment"""
import os
import ci_info

def test_circle():
    IS_REAL_PR = bool(
        os.getenv("GITHUB_EVENT_NAME") and
        os.getenv("GITHUB_EVENT_NAME") == "pull_request"
    )
    assert ci_info.name() == "GitHub Actions"
    assert ci_info.is_ci() is True
    assert ci_info.is_pr() == IS_REAL_PR

    assert ci_info.info() == {
        "name": "GitHub Actions",
        "is_ci": True,
        "is_pr": IS_REAL_PR
    }
