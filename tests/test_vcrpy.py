import os
from unittest import mock
import pytest

from changelog.d_full_featured_facade import generate_changelog, GitHubClient


class GitHubClientStub:
    def __init__(self, commit_messages=None):
        self.commit_messages = commit_messages
        self.mock = mock.Mock()

    def get_release_date(self, *args, **kwargs):
        self.mock(*args, **kwargs)

    def get_commit_messages(self, *args, **kwargs):
        self.mock(*args, **kwargs)
        return self.commit_messages


@mock.patch("changelog.d_full_featured_facade.GitHubClient")
def test_generate_changelog(github_mock):
    commit_messages = ["first commit", "last commit"]
    github_mock.return_value = GitHubClientStub(commit_messages)

    messages = generate_changelog("owner", "repo", "1.0.0")

    assert messages == ["CHANGELOG", "", "- first commit", "- last commit"]


@pytest.mark.vcr(cassette_library_dir="tests/cassettes/rest")
def test_github_client_get_release_date():
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)
    github = GitHubClient(GITHUB_TOKEN)
    release_dt = github.get_release_date("busy-beaver-dev", "busy-beaver", "1.3.2")

    assert release_dt == "2020-01-26T19:04:10Z"


@pytest.mark.vcr(cassette_library_dir="tests/cassettes/rest")
def test_github_client_get_commit_messages():
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)
    github = GitHubClient(GITHUB_TOKEN)

    release_dt = "2020-01-25T19:04:10Z"
    messages = github.get_commit_messages("busy-beaver-dev", "busy-beaver", release_dt)

    assert "Update to Python 3.9 (#335)" in messages
