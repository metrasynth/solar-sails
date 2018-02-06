import os

__version__ = '0.1.1'


def build_number():
    travis_commit = os.environ.get('TRAVIS_COMMIT', None)
    appveyor_commit = os.environ.get('APPVEYOR_REPO_COMMIT', None)
    commit = travis_commit or appveyor_commit or None
    if commit is not None:
        return '{}pre-{}'.format(__version__, commit[:7])
    else:
        return __version__
