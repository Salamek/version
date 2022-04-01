
from distutils.version import StrictVersion
from typing import Generator
from version.commit_parser.models import ParsedVersion


class IChangeLog:
    def get_last_version(self) -> StrictVersion:
        raise NotImplementedError

    def generate(self, parsed_versions: Generator[ParsedVersion, None, None], return_only: bool = False) -> str:
        raise NotImplementedError
