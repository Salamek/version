from dataclasses import dataclass
from typing import List
from version.StrictVersion import StrictVersion
from version.enums.CommitTypeEnum import CommitTypeEnum


@dataclass
class ParsedCommit:
    revision: str
    description: str


@dataclass
class ParsedCommitGroup:
    parsed_commits: List[ParsedCommit]
    name: str = None


@dataclass
class ParsedCommitType:
    commit_type_enum: CommitTypeEnum
    parsed_commit_groups: List[ParsedCommitGroup]


@dataclass
class ParsedVersion:
    version: StrictVersion
    parsed_commit_types: List[ParsedCommitType]

