from typing import Tuple
from packaging.version import Version


class StrictVersion(Version):

    def _new_from_release(self, release: Tuple[int, ...]) -> "StrictVersion":
        # __replace__ returns a Version, so we re-wrap it
        new = self.__replace__(release=release)
        return StrictVersion(str(new))

    def advance_major(self, by: int = 1) -> 'StrictVersion':
        """
        Advance major version number
        :param by: step to advance
        :return: StrictVersion
        """
        major = self.major + by

        release = (major, 0, 0)

        return self._new_from_release(release)

    def advance_minor(self, by: int = 1) -> 'StrictVersion':
        """
        Advances minor version number
        :param by: step to advance
        :return: StrictVersion
        """
        minor = self.minor + by

        release = (self.major, minor, 0)

        return self._new_from_release(release)

    def advance_patch(self, by: int = 1) -> 'StrictVersion':
        """
        Advances patch version number
        :param by: step to advance
        :return: StrictVersion
        """
        micro = self.micro + by

        release = (self.major, self.minor, micro)

        return self._new_from_release(release)
