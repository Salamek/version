import os
import re
import datetime
from typing import Union
from git import Git
from distutils.version import StrictVersion
from version.change_log.IChangeLog import IChangeLog
from version.enums.CommitTypeEnum import CommitTypeEnum


class Debian(IChangeLog):
    def __init__(self, git: Git, change_log_file: str, message_types: list=None, project_name: str=None, stability: str=None, urgency: str=None):
        self.last_version_regex = re.compile(
            r'\((?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)\)\s+(?P<stability>\S+);\s+urgency=(?P<urgency>\S+)',
            re.MULTILINE
        )

        self.git = git
        self.change_log_file = change_log_file
        self.message_types = message_types
        self.project_name = project_name
        self.stability = stability if stability else 'unstable'
        self.urgency = urgency if urgency else 'medium'
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
        with open(self.change_log_file, 'r') as f:
            matches = self.last_version_regex.findall(f.read())
            if not matches:
                return None
            major, minor, patch, stability, urgency = matches[0]

            return StrictVersion('{}.{}.{}'.format(major, minor, patch))

    def generate(self, change_log: dict, version: StrictVersion,  return_only: bool=False) -> str:
        rows = [
            '{} ({}) {}; urgency={}'.format(self.project_name, version, self.stability, self.urgency),
            ''
        ]

        if not change_log:
            rows.append('  * Nothing worth mentioning')
        for commit_type, groups in change_log.items():
            if commit_type not in self.message_types:
                continue
            rows.append('  * {}'.format(self.commit_type_names.get(commit_type, commit_type)))
            for group_name, group_items in groups.items():
                rows.append('    * {}'.format(group_name))
                for item in group_items:
                    rows.append('      * {}'.format(item))

        rows.append('')
        rows.append(' -- {} <{}>  {}'.format(self.git.config(['user.name']), self.git.config(['user.email']), datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")))
        rows.append('')
        rows.append('')

        new_content = '\n'.join(rows)

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
