# Version
Do you know that boring step before pushing new relese ? Yes changing version strings all over the place :-( Well this tool solves that for you!
Version is simple tool to manage multiple version files in your project and commit/tag/push them to git repository.

# Features

1. Modifies all files containing version string with one simple command
2. Adds modified version files into GIT commit and pushes them
3. Can create version tag in GIT
4. Keeps track if all version files uses same version string
5. Keeps track if all modified files are commited to GIT
6. Keeps track if newly set version is not lower of equal to current version
7. Checks validity of newly set version
8. Can advance patch/minor/major version by simply using "+" notation (see usage section)
9. Currently this tool assumes that you are using GIT as your VCS, if do you wish to use this tool without GIT or with different VCS let me know in Issue.
10. It can generate CHANGELOG using specified commit parser and changelog generator

# Installation

## Debian and derivates

Add repository by running these commands

```bash
$ wget -O - https://apt.salamek.cz/apt/conf/salamek.gpg.key|sudo apt-key add -
$ echo "deb     https://apt.salamek.cz/apt all main" | sudo tee /etc/apt/sources.list.d/salamek.cz.list
```

And then you can install a package `version`

```bash
$ apt update && apt install version
```

## Archlinux

Add repository by adding this at end of file /etc/pacman.conf

```
[salamek]
Server = https://arch.salamek.cz/any
SigLevel = Optional
```

and then install by running

```bash
$ pacman -Sy version
```

# Configuration

Create file named `.version.yml` in root of your project with this content (Only REGEXPS and VERSION_FILES are required):

```yml

# GIT Configuration
GIT:
    AUTO_COMMIT: true # Autocommit modified version files (default: true)
    AUTO_TAG: true # Create GIT tag with new version (default: true)
    AUTO_PUSH: true # Automaticaly push to repository false=disabled, true=enabled, 'remote_name'=enabled and push to remote_name (default: true)
    COMMIT_MESSAGE: 'New version {version}' # Message used in commit {version} is placeholder for new version string (default: 'New version {version}')

# Array of regexps used to find version strings in your VERSION_FILES
# key is name of regexp and value is regexp it self
# add your own and delete unused ones
REGEXPS:
    'python': __version__\s*=\s*\'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)\' # Regexp for version format commonly used in python
    'setup.py': version\s*=\s*\'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)\' # Regexp for version format commonly used in python setup.py
    'PKGBUILD': pkgver\s*=\s*(?P<version>.*) # Regexp used in PKGBUILD

# Array of version files to find and modify, glob format is supported
# key is glob path and values is regexp name to use to find version string in found file/s
# add your own and delete unused ones
VERSION_FILES:
    'version/__init__.py': 'python'
    'setup.py': 'setup.py'
    'archlinux/PKGBUILD': 'PKGBUILD'

# Change log generator
CHANGE_LOGS:
    'debian/changelog': # Relative change log path
        'generator': 'version.change_log.Debian' # Generator to use
        'types': ['fix', 'feat'] # Types of commits to use
        'arguments': # Special arguments for generator (in this case 'version.change_log.Debian')
            'project_name': 'attendance-gui'
            'stability': 'unstable'
            'urgency': 'medium'

```

# Usage

In your project root, you can run these basic commands:

To show current version (finds all version files and versions inside them and compare, if all versions match show it)
```bash
$ version
OR
$ version status
```

To set new version
```bash
$ version 1.0.1
OR
$ version mark 1.0.1
```

To simply advance in version you can use `"+"` notation in format `(+{1-3})({\d+})` where first group defines version type (number of +) and second version defines step:

* `+` Means advance by one patch version
* `++` Means advance by one minor version
* `+++` Means advance by one major version
* `+2` Means advance by two patch version
* `++2` Means advance by two minor version
* `+++2` Means advance by two major version
* ...

```bash
$ version + #to advance by 1 patch version
OR
$ version +10 #to advance by 10 patch versions
OR
$ version ++1 #to advance by 1 minor version
```

For more options use

```bash
$ version --help
```

# Mirrors
This project is also mirrored to GitLab https://gitlab.com/Salamek/version

Thats it!
