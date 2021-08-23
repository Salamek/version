#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main entry-point into the 'version' application.

This is a version

License: GPL-3.0
Website: https://github.com/Salamek/version

Command details:
    mark                Mark project specified by --project_dir by <version>.
    status              Show current --project_dir version.


Usage:
    version mark <version> [-p DIR] [-c FILE] [--dry] [--all_yes] [--force]
    version status [-p DIR] [-c FILE]
    version 
    version <version> [-p DIR] [-c FILE] [--dry] [--all_yes] [--force]
    version (-h | --help)
    version (-v | --version)

Options:
    --dry                       Run as usually but don't change anything.
    -p DIR --project_dir=DIR    Project directory, if not set current is used.
    -y --all_yes                Answer YES to all prompts.
    -f --force                  Force command when possible.
    -d --project_dir=DIR        Project directory, if not set current is used.
    -c FILE --config_file=FILE  Path to config file, if not set --project_dir/version.conf is used
    --version                   Show version.
"""
import signal
import sys
import logging
from version.Version import Version
from version.logging.ColoredFormatter import ColoredFormatter

from docopt import docopt

logging_level = logging.INFO
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging_level)
fmt = '[%(levelname)-18s] $BOLD%(asctime)s.%(msecs).03d %(process)d %(filename)s:$RESET%(lineno)d] %(message)s'
datefmt = '%m%d %H:%M:%S'
console_handler.setFormatter(ColoredFormatter(fmt, datefmt))

LOG = logging.getLogger()
LOG.setLevel(logging_level)
LOG.addHandler(console_handler)


def main() -> None:
    """
    Main entry point
    :return: 
    """
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0))  # Properly handle Control+C
    options = docopt(__doc__)

    version = Version(options)

    LOG.info('Current working directory is {}'.format(version.get_project_dir()))
    LOG.info('Current configuration is from {}'.format(version.get_config_file()))
    LOG.debug('Current configuration is: {}'.format(version.get_config()))
    LOG.debug('Current options are: {}'.format(options))

    if options['<version>']:
        if options['<version>'] == 'mark':
            print('Please specify mark version')
        else:
            version.mark()
    elif not options['<version>'] or options['status']:
        version.status()


if __name__ == '__main__':
    main()
