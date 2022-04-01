
from typing import Generator
from version.commit_parser.models import ParsedVersion


class ICommitParser:
    # def __init__(self, git: Git, from_version: StrictVersion=None):
    #    raise NotImplementedError

    def get_parsed_versions(self) -> Generator[ParsedVersion, None, None]:
        raise NotImplementedError
