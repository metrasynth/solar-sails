import os

__version__ = '0.1.1'


def build_number():
    github_sha = os.environ.get('GITHUB_SHA', None)
    appveyor_commit = os.environ.get('APPVEYOR_REPO_COMMIT', None)
    commit = github_sha or appveyor_commit or None
    if commit is not None:
        return '{}pre-{}'.format(__version__, commit[:7])
    else:
        return __version__
