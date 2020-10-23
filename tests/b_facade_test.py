from unittest import mock
import responses

from changelog.b_facade import generate_changelog, GitHubClient


@responses.activate
def test_github_client_get_release_date():
    responses.add(
        responses.GET,
        "https://api.github.com/repos/owner/repo/releases/tags/1.0.0",
        json={"published_at": "2020-01-26"},
    )

    github = GitHubClient()
    release_dt = github.get_release_date("owner", "repo", "1.0.0")

    assert release_dt == "2020-01-26"


@responses.activate
def test_github_client_get_commit_messages():
    responses.add(
        responses.GET,
        "https://api.github.com/repos/owner/repo/commits",
        json=[
            {"commit": {"message": "last commit"}},
            {"commit": {"message": "first commit"}},
        ],
    )

    github = GitHubClient()
    messages = github.get_commit_messages("owner", "repo", "release_dt")

    assert messages == ["first commit", "last commit"]


class GitHubClientStub:
    def __init__(self, commit_messages=None):
        self.commit_messages = commit_messages
        self.mock = mock.Mock()

    def get_release_date(self, *args, **kwargs):
        self.mock(*args, **kwargs)

    def get_commit_messages(self, *args, **kwargs):
        self.mock(*args, **kwargs)
        return self.commit_messages


@mock.patch("changelog.b_facade.GitHubClient")
def test_generate_changelog(github_mock):
    commit_messages = ["first commit", "last commit"]
    github_mock.return_value = GitHubClientStub(commit_messages)

    messages = generate_changelog("owner", "repo", "1.0.0")

    assert messages == ["CHANGELOG", "", "- first commit", "- last commit"]
