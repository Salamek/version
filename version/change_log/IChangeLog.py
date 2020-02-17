
from distutils.version import StrictVersion


class IChangeLog:
    def get_last_version(self) -> StrictVersion:
        raise NotImplementedError

    def generate(self, change_log: dict, version: StrictVersion, return_only: bool = False) -> str:
        raise NotImplementedError
