
from git import Git
from distutils.version import StrictVersion


class ICommitParser:
    # def __init__(self, git: Git, from_version: StrictVersion=None):
    #    raise NotImplementedError

    def get_change_log(self) -> dict:
        raise NotImplementedError
