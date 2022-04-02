import os
import re
import datetime
import json
from typing import Union, Generator, List, Tuple
from git import Git
from distutils.version import StrictVersion
from version.commit_parser.models import ParsedVersion
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

    def _get_tag_info(self, tag_version: StrictVersion) -> Union[Tuple[str, str, datetime.datetime], None]:
        result = self.git.for_each_ref([
            'refs/tags/{}'.format(str(tag_version)),
            '--format={\"taggerdate\": \"%(taggerdate)\", \"taggeremail\": \"%(taggeremail)\", \"taggername\": \"%(taggername)\"}'])

        if not result:
            return None

        tag_info = json.loads(result)
        taggername = tag_info.get('taggername')
        taggeremail = tag_info.get('taggeremail')
        taggerdate = tag_info.get('taggerdate')
        if not taggername or not taggeremail or not taggerdate:
            return None

        return taggername, taggeremail.replace('<', '').replace('>', ''), datetime.datetime.strptime(taggerdate, '%a %b %d %H:%M:%S %Y %z')

    def get_last_version(self) -> Union[StrictVersion, None]:
        try:
            with open(self.change_log_file, 'r') as f:
                matches = self.last_version_regex.findall(f.read())
                if not matches:
                    return None
                major, minor, patch, stability, urgency = matches[0]

                return StrictVersion('{}.{}.{}'.format(major, minor, patch))
        except FileNotFoundError:
            return None

    def _generate_version_block(self, parsed_version: ParsedVersion) -> List[str]:
        rows = [
            '{} ({}) {}; urgency={}'.format(self.project_name, parsed_version.version, self.stability, self.urgency),
            ''
        ]

        rows_content = []
        for parsed_commit_type in parsed_version.parsed_commit_types:

            if parsed_commit_type.commit_type_enum not in self.message_types:
                continue
            rows_content.append('  * {}'.format(self.commit_type_names.get(parsed_commit_type.commit_type_enum, parsed_commit_type.commit_type_enum)))
            for parsed_commit_group in parsed_commit_type.parsed_commit_groups:
                rows_content.append('    * {}'.format(parsed_commit_group.name))
                for parsed_commit in parsed_commit_group.parsed_commits:
                    rows_content.append('      * {} {}'.format(parsed_commit.revision, parsed_commit.description))

        if not rows_content:
            rows.append('  * Nothing worth mentioning')
        else:
            rows.extend(rows_content)

        rows.append('')

        tag_info = self._get_tag_info(parsed_version.version)
        if tag_info:
            name, email, date = tag_info
        else:
            name = self.git.config(['user.name'])
            email = self.git.config(['user.email'])
            date = datetime.datetime.now(datetime.timezone.utc)

        rows.append(' -- {} <{}>  {}'.format(
            name,
            email,
            date.strftime("%a, %d %b %Y %H:%M:%S %z"))
        )

        rows.append('')
        rows.append('')

        return rows

    def generate(self, parsed_versions: Generator[ParsedVersion, None, None], return_only: bool = False) -> str:
        rows = []
        for parsed_version in parsed_versions:
            rows.extend(self._generate_version_block(parsed_version))

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
