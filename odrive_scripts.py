#!/usr/bin/python
import logging
import os
from glob import glob
import argparse

import odrive

logger = logging.getLogger()
cur_path = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.abspath(os.path.join(cur_path, os.pardir, 'log'))
log_file = os.path.join(log_dir, 'scripts.log')
logging.basicConfig(filename=log_file, filemode='w', level=logging.DEBUG)

logger.info('Reading server ports')
AGENT_PORT_REGISTRY_FILE_PATH = os.path.join(odrive.expand_user('~'), '.odrive-agent', '.oreg')
DESKTOP_PORT_REGISTRY_FILE_PATH = os.path.join(odrive.expand_user('~'), '.odrive', '.oreg')
agentProtocolServerPort = odrive.get_protocol_server_port(AGENT_PORT_REGISTRY_FILE_PATH)
desktopProtocolServerPort = odrive.get_protocol_server_port(DESKTOP_PORT_REGISTRY_FILE_PATH)
logger.info('Finished reading server ports')


def log_function_call(func):
    logger.info('Start {}'.format(func))
    func()
    logger.info('Finished {}'.format(func))


def unsync_object(path):
    """Unsync file or folder in path """
    logger.info('Unsyncing {}'.format(path))
    try:
        command = odrive.Unsync(agentPort=agentProtocolServerPort,
                                desktopPort=desktopProtocolServerPort,
                                path=path)
        command.execute()

    except Exception:
        logger.error(
            'An error occured while unsyncing {}'.format(path),
            exc_info=True)
        raise


def unsync_objects(paths):
    """ Unsync all folders and files given in paths """
    for p in paths:
        unsync_object(p)


def sync_placeholder(placeholder_path, only_folders=False):
    """ Synchronize placeholder """
    logger.debug('Starting placeholder syncing with placeholder'
                 '="{}" and only_folders={}'.format(placeholder_path, only_folders))
    path, extension = os.path.splitext(placeholder_path)
    try:
        is_file = extension == '.cloud'
        if only_folders and is_file:
            return
        logger.info('Syncing {}'.format(placeholder_path))
        command = odrive.Sync(agentPort=agentProtocolServerPort,
                              desktopPort=desktopProtocolServerPort,
                              placeholderPath=placeholder_path)
        command.execute()
    except Exception:
        logger.error(
            'An error occured while syncing {}'.format(placeholder_path),
            exc_info=True)
        raise


def is_placeholder(path):
    path, extension = os.path.splitext(path)
    if extension in ['.cloud', '.cloudf']:
        return (True, path, extension)


def traverse_and_sync(root, only_folders=False, max_depth=-1):
    """
    Recursively syncs all files and folders from the root directory.
    If the root is a placeholder itself it will first be synced.


    Parameters
    ----------------
    root :  String
            Path to the root directory
    only_folders :  Boolean (default=False)
                    If True only folders are synced.
    max_depth :     Integer (default=-1)
                    If -1 all subdirectories from root are synced
                    If zero only the root is synced
                    If positive only directories down to a depth of max_depth
                    from the root are synced.
    """

    path, extension = os.path.splitext(root)
    if extension in ['.cloud', '.cloudf']:
        logger.debug('Syncing root')
        sync_placeholder(root, only_folders=only_folders)
        root = path

    if max_depth == 0:
        logger.debug('Max depth reached. Returning')
        return

    for file_ in glob(os.path.join(root, '*.cloud*')):
        sync_placeholder(file_, only_folders)

    new_folders = next(os.walk(os.path.join(root, '.')))[1]

    new_max_depth = max([max_depth - 1, -1])

    if new_max_depth == 0:
        logger.debug('Max depth reached. Returning')
        return

    for folder in [os.path.join(root, f) for f in new_folders]:
        traverse_and_sync(folder, only_folders, max_depth=new_max_depth)


def sync(placeholders):
    """ Sync placeholders, but do not sync eventual children """
    for p in placeholders:
        sync_placeholder(p)


def sync_content(placeholders, max_depth=-1):
    """ Recursively sync directories and files in the placeholders and their children """
    for p in placeholders:
        logger.debug('Sync content of {}'.format(p))
        traverse_and_sync(p, max_depth=max_depth)


def sync_immediate_content(placeholders):
    """ Sync placeholders and their immediate children """
    sync_content(placeholders, max_depth=1)


def sync_immediate_folders(placeholders):
    """ Sync foldes and their immediate children """
    sync_folders(placeholders, max_depth=1)


def sync_folders(placeholders, max_depth=-1):
    """
    Sync all folders in the placeholders' directory trees.
    No files are synced.
    """
    for p in placeholders:
        traverse_and_sync(p, only_folders=True, max_depth=max_depth)


def main():
    command_dict = {
        'sync': sync,
        'sync_content': sync_content,
        'sync_immediate_content': sync_immediate_content,
        'sync_folders': sync_folders,
        'unsync': unsync_objects,
        'sync_immediate_folders': sync_immediate_folders
    }
    logger.info('Reading selected objects')
    paths = os.environ['NAUTILUS_SCRIPT_SELECTED_FILE_PATHS'].splitlines()

    logger.info('Reading arguments')
    arg_parser = argparse.ArgumentParser()
    possible_commands = ', '.join(command_dict.keys())
    arg_parser.add_argument('command', help='Which command to perform.'
                            'Choose between {}'.format(possible_commands))
    args = arg_parser.parse_args()
    logger.info('Command: {}'.format(args.command))
    command_dict[args.command](paths)


if __name__ == "__main__":
    logger.info('Starting operations')
    try:
        main()
    except:
        logger.error('An error occured', exc_info=1)
    else:
        logger.info('Done performing operations')
