# Using the Facade Pattern to Wrap Third-Party Integrations

Code and tests used to support blog post that demonstrates the advantages of using the Facade Pattern to wrap third-party integrations.

[Link to Blog Post]()

---

#### Table of Contents

<!-- TOC -->

- [Setting Up Development Environment](#setting-up-development-environment)
- [Project Description](#project-description)
- [Explanation of Code](#explanation-of-code)
  - [Directly Integrate with Requests](#directly-integrate-with-requests)
  - [Implement Facade](#implement-facade)
  - [GraphQL API](#graphql-api)
  - [Full Featured Facade](#full-featured-facade)
  - [VCR.py Integration Tests](#vcrpy-integration-tests)

<!-- /TOC -->

---

## Setting Up Development Environment

1. Create and activate Python 3.6+ virtual environment
1. `make install`

## Project Description

We will be creating a [changelog](https://en.wikipedia.org/wiki/Changelog) generator.

This will take the form of a command line application that takes arguments: `public repository` and `previous version`

- app grabs data from GitHub
- accepts a public repository and a previous release
- generate a CHANGELOG consisting of commit messages

## Explanation of Code

### Directly Integrate with Requests

> File: `changelog/a_direct_integration.py`

Use requests to hit endpoints
and collect information.

For tests we use responses to mock out
the external API call.
Tests depend on GitHub API implemtnation,
i.e. something we do not control.

If the API changes,
we have to modify our code AND tests.
Basically rewrite everything again
to ensure it works as expected.

This code is also hard to read,
we have to read thru each line to
understand what's going on.

### Implement Facade

> File: `changelog/b_facade.py`

Created a wrapper around the GitHub API.
Monkeypatch the GitHubClient with
a FkeGitHubClient stub to simplify tests.

### GraphQL API

> File: `changelog/c_graphql.py`

GraphQL allows us to get the exact information we need.
Just by swapping out the facade and facade tests,
we can use a different kind of API
without having to change business logic.

Integrating directly couples our code
to something we do not control.

### Full Featured Facade

> File: `changelog/d_session.py`

Everything is encapsulated in a class
that can hold state.
Create a
[requests.session](https://requests.readthedocs.io/en/master/user/advanced/)
and use headers effectively.
Also use a GitHub token we can use
to grab information from private repos.

### VCR.py Integration Tests

> File: `tests/vcr_test.py`

Replace responses-based unit tests
with VCR.py-based integration tests.

While we could use VCR.py for all of our tests,
I think it's better practice
to use it for integration tests around wrapper classes.
If underlying implementation changes,
we only have to worry about how it affects each Client library.
