import enum


@enum.unique
class CommitTypeEnum(enum.Enum):
    CHORE = 'chore'
    DOCS = 'docs'
    FEAT = 'feat'
    FIX = 'fix'
    REFACTOR = 'refactor'
    STYLE = 'style'
    TEST = 'test'
