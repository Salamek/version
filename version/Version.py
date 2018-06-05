import os
import yaml
import re
import glob
import logging
from git import Repo, Git
from version.exception import ConfigurationError, ProjectVersionError
from distutils.version import StrictVersion


class Version(object):
    """
    Version class
    """
    VERSION_CONF_NAME = '.version.yml'
    log = logging.getLogger(__name__)

    _regexps = {}

    def __init__(self, options):
        """
        Constructor
        :param options: options passed by user 
        """
        self._options = options
        self._project_dir = self._resolve_project_dir()
        self._config_file = self._resolve_config_file()
        self._config = self._load_config()
        self.validate_config(self._config)

        self.compile_regexps()

    def compile_regexps(self) -> None:
        """
        Precompile regexps
        :return: 
        """
        for name, regexp in self._config['REGEXPS'].items():
            self._regexps[name] = re.compile(regexp, re.MULTILINE)

    @staticmethod
    def validate_config(config_dict: dict) -> None:
        """
        Validate configuration
        :param config_dict: dict containing configuration
        :return: 
        """
        if 'VERSION_FILES' not in config_dict:
            raise ConfigurationError('Required config section VERSION_FILES not found in config')

        if not len(config_dict['VERSION_FILES']):
            raise ConfigurationError('Required config section VERSION_FILES is empty')

        if not len(config_dict['REGEXPS']):
            raise ConfigurationError('Required config section REGEXPS is empty')

        # Check if all files have valid regexp names
        for file, regexp_name in config_dict['VERSION_FILES'].items():
            if regexp_name not in config_dict['REGEXPS']:
                raise ConfigurationError('Regexp name {} not found for file {}'.format(regexp_name, file))

    def get_project_dir(self) -> str:
        """
        Return project dir
        :return: 
        """
        return self._project_dir

    def _resolve_project_dir(self) -> str:
        """
        Finds project dir by option in configuration or by passed parameter
        :return: 
        """
        if self._options['--project_dir']:
            project_dir = os.path.dirname(os.path.realpath(self._options['--project_dir']))
            if not os.path.isdir(project_dir):
                raise ConfigurationError('Project DIR {} resolved to {} not found'.format(
                    self._options['--project_dir'],
                    project_dir
                ))
        else:
            project_dir = os.getcwd()

        return project_dir

    def get_config_file(self) -> str:
        """
        Return config file
        :return: 
        """
        return self._config_file

    def _resolve_config_file(self) -> str:
        """
        Find config file in default location (project root) or by passed argument
        :return: 
        """
        if self._options['--config_file']:
            config_file = os.path.realpath(self._options['--config_file'])
            if not os.path.isfile(config_file):
                raise ConfigurationError('Project config file {} resolved to {} not found'.format(
                    self._options['--config_file'],
                    config_file
                ))
        else:
            config_file = os.path.join(self.get_project_dir(), self.VERSION_CONF_NAME)
            if not os.path.isfile(config_file):
                raise ConfigurationError('Project config file not found'.format(
                    config_file
                ))

        return config_file

    def get_config(self) -> dict:
        """
        Return config
        :return: 
        """
        return self._config

    def _load_config(self) -> dict:
        """
        Load config from file into private variable
        :return: 
        """
        with open(self.get_config_file(), 'rb') as config_file_handle:
            config = yaml.load(config_file_handle)

            # Default options
            config['GIT'] = config.get('GIT', {})
            config['GIT']['AUTO_COMMIT'] = config['GIT'].get('AUTO_COMMIT', True)
            config['GIT']['AUTO_TAG'] = config['GIT'].get('AUTO_TAG', True)
            config['GIT']['AUTO_PUSH'] = config['GIT'].get('AUTO_PUSH', True)
            config['GIT']['COMMIT_MESSAGE'] = config['GIT'].get('COMMIT_MESSAGE', 'New version {version}')

            return config

    def find_version(self) -> StrictVersion:
        """
        Find project current version and check for mismatch
        :return: StrictVersion
        """
        versions = {}
        for path, regexp_name in self._config['VERSION_FILES'].items():
            full_path = os.path.join(self._project_dir, path)
            version_regexp = self._regexps[regexp_name]
            glob_result = glob.iglob(full_path, recursive=True)
            if not glob_result:
                self.log.warning('No files found for path {}'.format(full_path))
            for found_path in glob_result:
                with open(found_path) as found_path_handle:
                    # lets find if it contains regexp
                    version_match = version_regexp.search(found_path_handle.read())
                    if not version_match:
                        self.log.warning('No version match for file {} with regexp named "{}"'.format(found_path, regexp_name))
                    else:
                        try:
                            # Lets try full version group
                            vstring = version_match.group('version')
                        except IndexError:
                            # Lets try parted version match
                            (major, minor) = version_match.group('major', 'minor')

                            try:
                                version = tuple(map(int, [major, minor, version_match.group('patch')]))
                            except IndexError:
                                version = tuple(map(int, [major, minor])) + (0,)

                            try:
                                prerelease = (version_match.group('prerelease')[0], int(version_match.group('prerelease_num')))
                            except IndexError:
                                prerelease = None

                            # Build valid version string
                            vstring = '.'.join(map(str, version))

                            if prerelease:
                                vstring = vstring + prerelease[0] + str(prerelease[1])

                        if found_path not in versions:
                            corrected_version = str(StrictVersion(vstring))
                            versions[found_path] = corrected_version
                            self.log.info('Found version file {} with version {}'.format(
                                found_path,
                                vstring if vstring == corrected_version else '{} (corrected to {})'.format(vstring, corrected_version)
                            ))

        if not len(versions):
            raise ProjectVersionError('No version files found!')

        # Make sure that all found versions match
        unique_versions = set(versions.values())
        if len(unique_versions) > 1:
            for unique_version in unique_versions:
                for file_path in [k for k,v in versions.items() if v == unique_version]:
                    self.log.error('File {} have different version than others {}'.format(
                        file_path,
                        unique_version)
                    )

            raise ProjectVersionError

        return StrictVersion(next(iter(versions.values())))

    def mark_version_files(self, version: StrictVersion, dry: bool=False) -> list:
        """
        Mark version files with specified version
        :param version: version to set
        :param dry: is dry run ?
        :return: list
        """
        processed_files = []
        modified_files = []
        for path, regexp_name in self._config['VERSION_FILES'].items():
            full_path = os.path.join(self._project_dir, path)
            version_regexp = self._regexps[regexp_name]
            glob_result = glob.iglob(full_path, recursive=True)
            if not glob_result:
                self.log.warning('No files found for path {}'.format(full_path))
            for found_path in glob_result:
                if found_path not in processed_files:
                    with open(found_path, 'r') as found_path_handle_read:
                        # lets find if it contains regexp
                        if dry:
                            if not version_regexp.search(found_path_handle_read.read()):
                                self.log.warning('No version match for file {}'.format(found_path))
                            else:
                                self.log.info('DRY RUN: I would modify {} to {}'.format(found_path, version))
                            modified_data_to_write = None
                        else:
                            def replace_function(m):
                                full_match = m.group(0)
                                replaces = []
                                try:
                                    # Lets try full version group
                                    replaces.append([m.group('version'), str(version)])
                                except IndexError:
                                    # Lets try parted version match
                                    replaces.append([m.group('major'), str(version.version[0])])
                                    replaces.append([m.group('minor'), str(version.version[1])])
                                    try:
                                        replaces.append([m.group('patch'), str(version.version[2])])
                                    except IndexError:
                                        pass

                                    try:
                                        if version.prerelease:
                                            replaces.append([m.group('prerelease'), str(version.prerelease[0])])
                                            replaces.append([m.group('prerelease_num'), str(version.prerelease[1])])
                                        else:
                                            replaces.append([m.group('prerelease'), ''])
                                            replaces.append([m.group('prerelease_num'), ''])
                                    except IndexError:
                                        pass

                                search_after = 0
                                for needle, replacement in replaces:
                                    index = full_match.find(needle, search_after)
                                    if index > -1:
                                        search_after = index + 1
                                        keep_part = full_match[:index]
                                        replace_part = full_match[index:]
                                        full_match = keep_part + replace_part.replace(needle, replacement, 1)

                                return full_match
                            modified_data_to_write = version_regexp.sub(replace_function, found_path_handle_read.read())
                    if modified_data_to_write:
                        with open(found_path, 'w') as found_path_handle_write:
                            found_path_handle_write.write(modified_data_to_write)
                            modified_files.append(found_path)
                            # Append to processed list to prevent multiple file changes
                    processed_files.append(found_path)

        return modified_files

    @staticmethod
    def advance_patch(version: StrictVersion, by: int=1) -> StrictVersion:
        """
        Advances patch version number 
        :param version: version to modify
        :param by: step to advance
        :return: StrictVersion
        """
        new_version = StrictVersion(str(version))
        version_modify = list(new_version.version)
        version_modify[2] = version_modify[2] + by
        new_version.version = tuple(version_modify)

        return new_version

    @staticmethod
    def advance_minor(version: StrictVersion, by: int=1) -> StrictVersion:
        """
        Advances minor version number
        :param version: version to modify
        :param by: step to advance
        :return: StrictVersion
        """
        new_version = StrictVersion(str(version))
        version_modify = list(new_version.version)
        version_modify[1] = version_modify[1] + by
        version_modify[2] = 0
        new_version.version = tuple(version_modify)

        return new_version

    @staticmethod
    def advance_major(version: StrictVersion, by: int=1) -> StrictVersion:
        """
        Advance major version number
        :param version: version to modify
        :param by: step to advance
        :return: StrictVersion
        """
        new_version = StrictVersion(str(version))
        version_modify = list(new_version.version)
        version_modify[0] = version_modify[0] + by
        version_modify[1] = 0
        new_version.version = tuple(version_modify)

        return new_version

    def build_commit_message(self, version: StrictVersion) -> str:
        """
        Build commit message
        :param version: version to put into commit message
        :return: str
        """
        return self._config['GIT']['COMMIT_MESSAGE'].format(version=version)

    def get_uncommited_modified_files(self) -> list:
        """
        Return uncommited modified files
        :return: list
        """
        git = Git(self._project_dir)
        return git.ls_files('-m').splitlines()

    def mark(self) -> None:
        """
        Mark project version files vit version specified by argument
        :return: None
        """
        # Check if we have all files commited
        modified_files = self.get_uncommited_modified_files()
        if len(modified_files):
            self.log.error('There are modified files that are not commited! {}'.format(modified_files))
            return

        current_version = self.find_version()

        if self._options['<version>'].startswith('+'):
            modifier = {
                1: self.advance_patch,
                2: self.advance_minor,
                3: self.advance_major,
            }.get(self._options['<version>'].count('+'))

            if not modifier:
                self.log.error('Wrong number of "+"')
                return
            by = 1
            found_by = re.match(r'^\+{1,3}(\d+)$', self._options['<version>'])
            if found_by:
                by = int(found_by.group(1))

            set_version = modifier(current_version, by)
        else:
            try:
                set_version = StrictVersion(self._options['<version>'])
            except ValueError:
                self.log.error('Invalid version string {}'.format(self._options['<version>']))
                return

        if current_version >= set_version:
            self.log.error('Current version is >= to new version ({} >= {})'.format(
                current_version,
                set_version
            ))
            return

        print('Change version form {} to {} ?'.format(current_version, set_version))
        if self._options['--dry']:
            self.log.warning('THIS IS DRY RUN, NOTHING WILL BE CHANGED')
        if self._config['GIT']['AUTO_COMMIT']:
            print('GIT.AUTO_COMMIT is ENABLED')
        if self._config['GIT']['AUTO_TAG']:
            print('GIT.AUTO_TAG is ENABLED')
        if self._config['GIT']['AUTO_PUSH']:
            print('GIT.AUTO_PUSH is ENABLED')
        print('GIT.COMMIT_MESSAGE will be "{}"'.format(
            self.build_commit_message(set_version)
        ))

        if self._options['--all_yes']:
            self.log.debug('Auto YES')
        else:
            ok = input('(y/n) [y]') or 'y'
            if ok.strip() == 'n':
                print('Maybe next time... BYE!')
                return
        modified_files = self.mark_version_files(set_version, dry=self._options['--dry'])
        self.log.debug('Modified files: {}'.format(modified_files))
        self.log.info('{} files has been modified to contain version string {}'.format(len(modified_files), set_version))

        repo = Repo(self._project_dir)

        # first add all modified files

        if self._config['GIT']['AUTO_COMMIT']:
            repo.index.add(modified_files)

            repo.index.commit(self.build_commit_message(set_version))
            self.log.info('{} files has been commited'.format(len(modified_files)))

        if self._config['GIT']['AUTO_TAG']:
            repo.create_tag(str(set_version), message=self.build_commit_message(set_version))
            self.log.info('Tag {} has been created'.format(set_version))

        if self._config['GIT']['AUTO_PUSH'] is True:
            repo.remotes.origin.push()
            self.log.info('Changes has been pushed to origin')
            repo.remotes.origin.push(str(set_version))
            self.log.info('Tag has been pushed to origin')
        elif isinstance(self._config['GIT']['AUTO_PUSH'], str):
            origin = getattr(repo.remotes, self._config['GIT']['AUTO_PUSH'])
            if not origin.exists():
                raise ConfigurationError('Push origin {} not found'.format(self._config['GIT']['AUTO_PUSH']))

            origin.push()
            self.log.info('Changes has been pushed to {}'.format(self._config['GIT']['AUTO_PUSH']))
            origin.push(str(set_version))
            self.log.info('Tag has been pushed to {}'.format(self._config['GIT']['AUTO_PUSH']))

    def status(self) -> None:
        """
        Print version status
        :return: 
        """
        print('Current version is {}'.format(self.find_version()))
