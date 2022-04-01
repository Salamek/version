
import re
import logging
from typing import List, Generator, Tuple
from git import Git, exc
from distutils.version import StrictVersion
from version.commit_parser.ICommitParser import ICommitParser
from version.enums.CommitTypeEnum import CommitTypeEnum
from version.commit_parser.models import ParsedVersion, ParsedCommitGroup, ParsedCommit, ParsedCommitType


class Sematic(ICommitParser):
    log = logging.getLogger(__name__)

    def __init__(self, git: Git, from_version: StrictVersion = None, to_version: StrictVersion = None):
        self.git = git

        self.from_version = from_version
        self.to_version = to_version
        self.regex = re.compile(r'^(\S{7})\s+(feat|fix|chore|refactor|docs|style|test)(?:\((\S+?)\):|:)\s+(.+)$', re.MULTILINE)

    def get_first_commit_hash(self):
        return self.git.rev_list(['--max-parents=0', 'HEAD'])

    def get_tags(self) -> List[StrictVersion]:
        tags_str = self.git.tag(['--sort=-committerdate']).splitlines()
        tags = [StrictVersion(tag_str) for tag_str in tags_str]
        tags.sort(reverse=True)
        return tags

    def get_tags_in_range(self, from_version: StrictVersion = None, to_version: StrictVersion = None) -> List[StrictVersion]:
        tags = self.get_tags()

        if from_version:
            tags = filter(lambda tag: tag >= self.from_version, tags)

        if to_version:
            tags = filter(lambda tag: tag <= self.to_version, tags)

        return list(tags)

    def get_tags_ranges(self, from_version: StrictVersion = None, to_version: StrictVersion = None) -> Generator[Tuple[str, str], None, None]:
        tags = self.get_tags_in_range(from_version, to_version)

        # Does to version exists in tags?
        # If it does not, use last tag + HEAD
        if self.to_version not in self.get_tags():
            # Requested to_version is in tags
            yield tags[0], 'HEAD'

        buffer = []
        for index, tag in enumerate(tags):
            if len(buffer) < 2:
                buffer.append(str(tag))
            else:
                buffer.reverse()
                yield tuple(buffer)
                buffer = [buffer[0]]

    def get_parsed_versions(self) -> Generator[ParsedVersion, None, None]:
        change_log = {}

        tags_ranges = self.get_tags_ranges(self.from_version, self.to_version)
        for from_version_str, to_version_str in tags_ranges:
            try:
                log = self.git.log(['{}...{}'.format(from_version_str, to_version_str), '--oneline'])
            except exc.GitCommandError as e:
                self.log.warning('Failed to fetch normal commit range, starting from first one: {}'.format(e))
                # we failed with specified from_version, lets check if from version is first commit and if not, lets try again or fail now
                first_commit = self.get_first_commit_hash()
                if first_commit == from_version_str:
                    raise e

                log = self.git.log(['{}...{}'.format(first_commit, to_version_str), '--oneline'])

            found_commits = self.regex.findall(log)
            for found_commit in found_commits:
                info_len = len(found_commit)
                if info_len == 3:
                    revision, commit_type, description = found_commit
                    commit_group = None
                elif info_len == 4:
                    revision, commit_type, commit_group, description = found_commit
                else:
                    continue

                commit_type_enum = CommitTypeEnum(commit_type)

                if not change_log.get(to_version_str):
                    change_log[to_version_str] = {}

                if not change_log.get(to_version_str, {}).get(commit_type_enum):
                    change_log[to_version_str][commit_type_enum] = {}

                if not change_log.get(to_version_str, {}).get(commit_type_enum, {}).get(commit_group):
                    change_log[to_version_str][commit_type_enum][commit_group] = []

                change_log[to_version_str][commit_type_enum][commit_group].append((revision, description))

        # Rework that shit ^ into dataclases
        for to_version_str, commit_types in change_log.items():
            parsed_commit_types = []
            for commit_type_enum, commit_groups in commit_types.items():
                parsed_commit_groups = []
                for commit_group, commits in commit_groups.items():
                    parsed_commit_groups.append(ParsedCommitGroup(
                        name=commit_group,
                        parsed_commits=[ParsedCommit(revision=revision, description=description) for revision, description in commits]
                    ))

                parsed_commit_types.append(ParsedCommitType(
                    commit_type_enum=commit_type_enum,
                    parsed_commit_groups=parsed_commit_groups
                ))

            yield ParsedVersion(
                version=self.to_version if to_version_str == 'HEAD' else StrictVersion(to_version_str),
                parsed_commit_types=parsed_commit_types
            )

