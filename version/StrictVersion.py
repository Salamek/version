from typing import Tuple
from packaging.version import Version, _Version, _cmpkey


class StrictVersion(Version):

    def _new_from_release(self, release: Tuple[int, int, int]) -> 'StrictVersion':
        new_version = StrictVersion(str(self))

        # Override internal version NamedTuple
        new_version._version = _Version(
            epoch=self._version.epoch,
            release=release,
            pre=self._version.pre,
            post=self._version.post,
            dev=self._version.dev,
            local=self._version.local,
        )

        # Override internal key
        new_version._key = _cmpkey(
            new_version._version.epoch,
            new_version._version.release,
            new_version._version.pre,
            new_version._version.post,
            new_version._version.dev,
            new_version._version.local,
        )

        return new_version

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
