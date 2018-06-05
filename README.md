# Version
Do you know that boring step before pushing new relese ? Yes changing version strings all over the place :-( Well this tool solves that for you!
Version is simple tool to manage multiple version files in your project and commit/tag/push them to git repository.

# Installation

## Debian and derivates

Add repository by running these commands

```bash
$ wget -O - https://apt.salamek.cz/apt/conf/salamek.gpg.key|sudo apt-key add -
$ echo "deb     https://apt.salamek.cz/apt all main" | sudo tee /etc/apt/sources.list.d/salamek.cz.list
```

And then you can install a package python3-blacklist

```bash
$ apt update && apt install python3-version
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

Create file named `.version.yml` in root of your project with this content:

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
    'python': '__version__\s*=\s*\'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)\'' # Regexp for version format commonly used in python
    'PKGBUILD': 'pkgver\s*=\s*(?P<version>.*)' # Regexp used in PKGBUILD

# Array of version files to find and modify, glob format is supported
# key is glob path and values is regexp name to use to find version string in found file/s
# add your own and delete unused ones
VERSION_FILES:
    'version/__init__.py': 'python'
    'archlinux/PKGBUILD': 'PKGBUILD'
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

To simply advance in version you can use "+" notation in format (+{1-3})({\d+}) where first group defines version type (number of +) and second version defines step:

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

Thats it!
