import os

from dotenv import load_dotenv

import logging
logger = logging.getLogger(__name__)

def read_apikey(apikey_conf) :
    home = os.getenv("HOME")
    
    config_list = [
        './config.conf',
        './.env',
        home + '/.opnsense/config.conf',
    ]

    if apikey_conf :
        config_list = [ apikey_conf ]

    configfile = None

    for filepath in config_list:
        logger.debug('search config candidate, {0}'.format(filepath))
        if os.path.exists(filepath) :
            configfile = filepath
            logger.debug('FOUND config candidate, {0}'.format(filepath))
            break
        else :
            logger.debug('NOT found config candidate, {0}'.format(filepath))
   
    if configfile :
        logger.debug('read config file as dotenv, {0}'.format(configfile))
        load_dotenv(dotenv_path=configfile)

