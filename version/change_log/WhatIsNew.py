import os
import re
from git import Git
from typing import Union, Generator, List
from distutils.version import StrictVersion
from version.change_log.IChangeLog import IChangeLog
from version.commit_parser.models import ParsedVersion
from version.enums.CommitTypeEnum import CommitTypeEnum


class WhatIsNew(IChangeLog):
    def __init__(self,
                 git: Git,
                 change_log_file: str,
                 message_types: list = None
                 ):
        self.last_version_regex = re.compile(
            r'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)',
            re.MULTILINE
        )
        self.git = git
        self.change_log_file = change_log_file
        self.message_types = message_types
        self.commit_type_names = {
            CommitTypeEnum.CHORE: '',
            CommitTypeEnum.DOCS: 'Documentation',
            CommitTypeEnum.FEAT: 'Features',
            CommitTypeEnum.FIX: 'Fixes',
            CommitTypeEnum.REFACTOR: 'Refactoring',
            CommitTypeEnum.STYLE: 'Styling',
            CommitTypeEnum.TEST: 'Tests',
        }

    def get_last_version(self) -> Union[StrictVersion, None]:
        # We will get last version from changelog
        try:
            with open(self.change_log_file, 'r') as f:
                matches = self.last_version_regex.findall(f.read())
                if not matches:
                    return None
                major, minor, patch = matches[0]

                return StrictVersion('{}.{}.{}'.format(major, minor, patch))
        except FileNotFoundError:
            return None

    def _generate_version_block(self, parsed_version: ParsedVersion) -> List[str]:
        rows = [
            '# What is new in version {} ?'.format(parsed_version.version),
            ''
        ]
        rows_content = []
        for commit_type in parsed_version.parsed_commit_types:
            if commit_type.commit_type_enum not in self.message_types:
                continue
            rows_content.append('  * {}'.format(self.commit_type_names.get(commit_type.commit_type_enum, commit_type.commit_type_enum)))
            for parsed_commit_group in commit_type.parsed_commit_groups:
                rows_content.append('    * {}'.format(parsed_commit_group.name))
                for parsed_commit in parsed_commit_group.parsed_commits:
                    rows_content.append('      * {} {}'.format(parsed_commit.revision, parsed_commit.description))

        if not rows_content:
            rows.append('  * Nothing worth mentioning :)')
        else:
            rows.extend(rows_content)

        rows.append('')
        rows.append('')

        return rows

    def generate(self, parsed_versions: Generator[ParsedVersion, None, None], return_only: bool = False) -> str:
        rows = []
        for parsed_version in parsed_versions:
            rows.extend(self._generate_version_block(parsed_version))

        new_content = '\n'.join(rows)
        print(new_content)

        if not return_only:
            dir_name = os.path.dirname(self.change_log_file)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)

            try:
                with open(self.change_log_file, 'r') as fr:
                    original_content = fr.read()
            except FileNotFoundError:
                original_content = ''

            with open(self.change_log_file, 'w') as fw:
                fw.write(new_content+original_content)

        return new_content
