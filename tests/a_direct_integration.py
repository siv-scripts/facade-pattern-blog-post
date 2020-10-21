import responses

from changelog.a_direct_integration import generate_changelog


@responses.activate
def test_generate_changelog():
    # Arrange -- created canned responses
    responses.add(
        responses.GET,
        "https://api.github.com/repos/owner/repo/releases/tags/1.0.0",
        json={"published_at": "2020-01-26"},
    )

    responses.add(
        responses.GET,
        "https://api.github.com/repos/owner/repo/commits",
        json=[
            {"commit": {"message": "last commit"}},
            {"commit": {"message": "first commit"}},
        ],
    )

    # Act
    changelog = generate_changelog("owner", "repo", "1.0.0")

    # Assert
    assert changelog == ["CHANGELOG", "", "- first commit", "- last commit"]
