#!/usr/bin/python
import logging
import os
from glob import glob
import argparse
import sys

import odrive

logger = logging.getLogger()
logging.basicConfig(filename='/home/simon/projects/bash/odrive/log', filemode='w', level=logging.INFO)

logger.info('Reading server ports')
AGENT_PORT_REGISTRY_FILE_PATH = os.path.join(odrive.expand_user('~'), '.odrive-agent', '.oreg')
DESKTOP_PORT_REGISTRY_FILE_PATH = os.path.join(odrive.expand_user('~'), '.odrive', '.oreg')
agentProtocolServerPort = odrive.get_protocol_server_port(AGENT_PORT_REGISTRY_FILE_PATH)
desktopProtocolServerPort = odrive.get_protocol_server_port(DESKTOP_PORT_REGISTRY_FILE_PATH)


def log_function_call(func):
    logger.info('Start {}'.format(func))
    func()
    logger.info('Finished {}'.format(func))


def sync_placeholder(placeholder_path, only_folders=False):
    """ Synchronize placeholder """
    logger.info('Syncing {}'.format(placeholder_path))
    path, extension = os.path.splitext(placeholder_path)
    try:
        is_file = extension == '.cloud'
        if only_folders and is_file:
            return

        command = odrive.Sync(agentPort=agentProtocolServerPort,
                              desktopPort=desktopProtocolServerPort,
                              placeholderPath=placeholder_path)
        command.execute()
    except Exception:
        logger.error(
            'An error occured while syncing {}'.format(placeholder_path),
            exc_info=True)
        raise


def traverse_and_sync(root, only_folders=False, max_depth=-1):
    """
    Recursively syncs all files and folders from the root directory.

    Parameters
    ----------------
    root :  String
            Path to the root directory
    only_folders :  Boolean (default=False)
                    If True only folders are synced.
    max_depth :     Integer (default=-1)
                    If -1 all subdirectories from root are synced
                    If non-zero only directories down to a depth of max_depth
                    from the root are synced.
    """
    for file_ in glob(os.path.join(root, '*.cloud*')):
        sync_placeholder(file_, only_folders)

    new_folders = next(os.walk(os.path.join(root, '.')))[1]

    new_max_depth = max([max_depth - 1, -2])
    if new_max_depth == -1:
        return

    for folder in [os.path.join(root, f) for f in new_folders]:
        traverse_and_sync(folder, only_folders, max_depth=new_max_depth)


def sync(placeholders):
    """ Sync placeholders, but do not sync eventual children """
    for p in placeholders:
        sync_placeholder(p)


def sync_content(placeholders, max_depth=-1):
    """ Recursivelt sync directories and files in the placeholders and their children """
    for p in placeholders:
        traverse_and_sync(p, max_depth)


def sync_immediate_content(placeholders):
    """ Sync placeholders and their immediate children """
    sync_content(placeholders, max_depth=1)


def sync_folders(placeholders):
    """
    Sync all folders in the placeholders' directory trees.
    No files are synced.
    """
    for p in placeholders:
        traverse_and_sync(p, only_folders=True)


def main():
    command_dict = {
        'sync': sync,
        'sync_content': sync_content,
        'sync_immediate_content': sync_immediate_content,
        'sync_folders': sync_folders
    }
    paths = os.environ['NAUTILUS_SCRIPT_SELECTED_FILE_PATHS'].splitlines()
    arg_parser = argparse.ArgumentParser()
    possible_commands = ', '.join(command_dict.items())
    arg_parser.add_argument('command', help='Which command to perform.'
                            'Choose between {}'.format(possible_commands))
    args = arg_parser.parse_args()
    try:
        command_dict[args.command](paths)
    except KeyError:
        print("Wrong command. Use the -h option for help.")
        sys.exit(1)
    except Exception:
        print(odrive.ERROR_SENDING_COMMAND)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
