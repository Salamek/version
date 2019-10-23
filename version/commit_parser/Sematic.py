
import re
import logging
from git import Git, exc
from distutils.version import StrictVersion
from version.commit_parser.ICommitParser import ICommitParser
from version.enums.CommitTypeEnum import CommitTypeEnum


class Sematic(ICommitParser):
    log = logging.getLogger(__name__)

    def __init__(self, git: Git, from_version: StrictVersion=None):
        self.git = git

        self.from_version = str(from_version)
        self.regex = re.compile(r'^(\S{7})\s+(feat|fix|chore|refactor|docs|style|test)(?:\((\S+?)\):|:)\s+(.+)$', re.MULTILINE)

    def get_first_commit_hash(self):
        return self.git.rev_list(['--max-parents=0', 'HEAD'])

    def get_change_log(self) -> dict:
        from_version = self.from_version
        if not from_version:
            from_version = self.get_first_commit_hash()

        try:
            log = self.git.log(['{}...HEAD'.format(from_version), '--oneline'])
        except exc.GitCommandError as e:
            self.log.warning('Failed to fetch normal commit range, starting from first one: {}'.format(e))
            # we failed with specified from_version, lets check if from version is first commit and if not, lets try again or fail now
            first_commit = self.get_first_commit_hash()
            if first_commit == from_version:
                raise e

            log = self.git.log(['{}...HEAD'.format(first_commit), '--oneline'])

        found_commits = self.regex.findall(log)
        change_log = {}
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

            if not change_log.get(commit_type_enum):
                change_log[commit_type_enum] = {}

            if not change_log.get(commit_type_enum, {}).get(commit_group):
                change_log[commit_type_enum][commit_group] = []

            change_log[commit_type_enum][commit_group].append('{} {}'.format(revision, description))

        return change_log
