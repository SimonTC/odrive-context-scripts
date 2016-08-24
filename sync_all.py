#!/home/simon/anaconda3/bin/python3.5
import os
import subprocess
import logging
import sys
import odrive

AGENT_PORT_REGISTRY_FILE_PATH = os.path.join(odrive.expand_user('~'), '.odrive-agent', '.oreg')
DESKTOP_PORT_REGISTRY_FILE_PATH = os.path.join(odrive.expand_user('~'), '.odrive', '.oreg')
agentProtocolServerPort = odrive.get_protocol_server_port(AGENT_PORT_REGISTRY_FILE_PATH)
desktopProtocolServerPort = odrive.get_protocol_server_port(DESKTOP_PORT_REGISTRY_FILE_PATH)




logger = logging.getLogger()
logging.basicConfig(filename='/home/simon/projects/bash/odrive/log', filemode='w', level=logging.INFO)

logger.info('Starting script')
logger.info('Python version: {}'.format(sys.version))
try:
    paths = os.environ['NAUTILUS_SCRIPT_SELECTED_FILE_PATHS'].splitlines()
except Exception as e:
    logger.error('Error', exc_info=1)
    raise
logger.info('Paths: {}'.format(paths))
for p in paths:
    logger.info('Looking at {}'.format(p))
    if os.path.splitext(p)[1] in ['.cloud', '.cloudf']:
        logger.info('Calling sync on {}'.format(p))
        try:
            command = odrive.Sync(agentPort=agentProtocolServerPort,
                                  desktopPort=desktopProtocolServerPort,
                                  placeholderPath=p)
            command.execute()

        except Exception as e:
            logger.error('Error while calling odrive', exc_info=1)
            logger.error(str(e.stderr))
            raise
logger.info('Done with syncing all files')
