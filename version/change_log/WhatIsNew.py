import os
from git import Git
from typing import Union
from distutils.version import StrictVersion
from version.change_log.IChangeLog import IChangeLog
from version.enums.CommitTypeEnum import CommitTypeEnum


class WhatIsNew(IChangeLog):
    def __init__(self,
                 git: Git,
                 change_log_file: str,
                 message_types: list = None
                 ):
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
        # We will get last version from git tag

        return StrictVersion(self.git.describe(abbrev=0))

    def generate(self, change_log: dict, version: StrictVersion, return_only: bool = False) -> str:
        rows = [
            'What is new in version {} ?'.format(version),
            ''
        ]

        if not change_log:
            rows.append('  * Nothing worth mentioning :)')
        for commit_type, groups in change_log.items():
            if commit_type not in self.message_types:
                continue
            rows.append('  * {}'.format(self.commit_type_names.get(commit_type, commit_type)))
            for group_name, group_items in groups.items():
                rows.append('    * {}'.format(group_name))
                for item in group_items:
                    rows.append('      * {}'.format(item))

        rows.append('')

        new_content = '\n'.join(rows)

        if not return_only:
            os.makedirs(os.path.dirname(self.change_log_file), exist_ok=True)
            with open(self.change_log_file, 'w') as fw:
                fw.write(new_content)

        return new_content
