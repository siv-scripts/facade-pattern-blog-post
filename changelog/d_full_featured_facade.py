import os
import argparse
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)
BASE_URL = "https://api.github.com"


def generate_changelog(owner, repo, version):
    github = GitHubClient(GITHUB_TOKEN)
    release_dt = github.get_release_date(owner, repo, version)
    commit_messages = github.get_commit_messages(owner, repo, release_dt)

    changelog = ["CHANGELOG", ""]
    for message in commit_messages:
        changelog.append(f"- {message}")
    return changelog


class GitHubClient:
    def __init__(self, oauth_token):
        headers = {
            "User-Agent": "Change Log",
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {oauth_token}",
            "Content-Type": "application/json",
        }
        session = requests.session()
        session.headers.update(headers)
        self.session = session

    def get_release_date(self, owner, repo, version):
        url = f"{BASE_URL}/repos/{owner}/{repo}/releases/tags/{version}"
        resp = self.session.get(url)
        if resp.status_code == 404:
            raise ValueError("Version does not exist")
        resp.raise_for_status()

        return resp.json()["published_at"]

    def get_commit_messages(self, owner, repo, release_dt):
        url = f"{BASE_URL}/repos/{owner}/{repo}/commits"
        params = {"sha": "master", "since": release_dt}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()

        messages = [item.get("commit", {}).get("message") for item in resp.json()]
        return messages[::-1]


def parse_args():
    description = "Generate changelog for repository"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-r",
        "--repo",
        type=str,
        help="Full path to repository, (abc/xyz)",
        required=True,
    )
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        help="Version to generate CHANGELOG from",
        required=True,
    )
    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_args()
    try:
        owner, repo = args["repo"].split("/")
    except ValueError:
        raise ValueError("Invalid repo")
    version = args["version"]

    changelog = generate_changelog(owner, repo, version)
    print()
    print("\n".join(changelog))
