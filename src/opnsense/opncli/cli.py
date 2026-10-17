#!/usr/bin/env python3

import sys
import os

import uuid
import re

import getopt
import yaml
import json

import ast
import pathlib
import importlib

import inspect

from dotenv import load_dotenv

import opnsense

PACKAGE_ROOT = pathlib.Path(opnsense.__file__).parent

#from opnsense.interfaces import InterfacesAPI

from opnsense.client import OPNsenseClient
from opnsense.firewall import FirewallAPI
#from opnsense.interfaces import InterfacesAPI
from opnsense.interfaces.vip_settings import VipSettingsAPI
from opnsense.firewall.category import CategoryAPI

from opnsense.utils.vip import vip_add, vip_clean, vip_list
from opnsense.utils.rule import rule_add, rule_clean, rule_list
from opnsense.utils.category import category_add, category_clean, category_list

from opnsense.utils.cli import *

#from opnsense.netsnmp.general import netsnmp_get, netsnmp_set
#from opnsense.netsnmp.service import netsnmp_reconfigure

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import logging
logger = logging.getLogger(__name__)

from opnsense.utils.optparser import *

from .usage import *

from pprint import pprint

no_argument       = 0
required_argument = 1
optional_argument = 2

def list_get(lst, idx, default):
    try:
        return lst[idx]
    except IndexError:
        return default

def main() :
    ret = 0
    
    output = None
    verify_ssl = False
    loglevel = 'info'
    #loglevel = 'debug'
    show_help = False
    show_longhelp = False
    apikey_conf = None
    config_conf = None

    args = []
    payload = {}
    params = {}
  
    long_options = [
        [ "help",   no_argument,       0, "h" ],
        [ "output", required_argument, 0, "o" ],
        [ "verify-ssl", required_argument, 0, None ],
        [ "loglevel",   required_argument, 0, "l" ],
        [ "apikey",   required_argument, 0, "a" ],
        [ "config",   required_argument, 0, "c" ],
        [ "target",   required_argument, 0, "t" ],
        [ None, 0, 0, None ],
    ]

    mod2ctl = {}

    path2cls = find_api_modules(
                    pathlib.Path(__file__).parent.parent,
                    PACKAGE_ROOT
                )
    logger.debug('path2cls is {0}'.format(path2cls))

    mod2ctl = find_controllers(path2cls)

    opts = {}
    params = {}
    data = {}
    non_opts = []

    i = 1
    while i < len(sys.argv) :
        i = parse_option(i, sys.argv,
                long_options, opts, params, data, non_opts)
        i = i + 1
    payload = data
    
    if ret != 0:
        sys.exit(1)
   
    if 'loglevel' in opts:
        loglevel = opts['loglevel']

    if loglevel in ('info'):
        level = logging.INFO
    elif loglevel in ('warn', 'warning') :
        level = logging.WARNING
    elif loglevel in ('debug'):
        print('DEBUG: enable debug', file=sys.stderr)
        level = logging.DEBUG
    elif loglevel in ('error'):
        level = logging.ERROR
    elif loglevel in ('critical'):
        level = logging.CRITICAL
    else :
        print('ERROR: unknown loglevel, {0}'.format(loglevel), file=sys.stderr)
        sys.exit(1)
    
    home = os.getenv("HOME")
    config_list = []
    config_list.append(       './config.conf')
    config_list.append(       './.env')
    config_list.append(home + '/.opnsense/config.conf')
    if apikey_conf:
        config_list.append(apikey_conf)
    if config_conf :
        config_list.append(config_conf)

    for filepath in config_list:
        logger.debug('config_list: {0}'.format(filepath))
        if os.path.exists(filepath) :
            logger.debug('read config "{0}"'.format(filepath))
            load_dotenv(dotenv_path=filepath)
    
    logger.debug('payload is {0}'.format(payload))
    
    # DEFAULT  level:name:message
    #format = '%(levelname)s:%(name)s:%(message)s'
    # CUSTOM (add space)
    #fmt = '%(levelname)s:%(name)s: %(message)s'
    fmt = '%(message)s'
    
    logging.basicConfig(level=level, format=fmt)

    if 'output' in opts:
        output = opts['output']

    if output :
        fp = open(output, mode='w', encoding='utf-8')
    else :
        fp = sys.stdout
  
    target = None
    module = None
    controller = None
    command = None

    optind = 0

    logger.debug('DEBUG: check "target" from option')
    target = opts.get('target', None)
    if not target :
        logger.debug('DEBUG: target is not defined in option')
        logger.debug('DEBUG: get target from environment variable')
        target = os.getenv("target")
        if target :
            logger.debug('DEBUG: got target, {0}'.format(target))
        else :
            logger.debug('DEBUG: not found target')

    module     = list_get(non_opts, optind, None)
    optind += 1
    controller = list_get(non_opts, optind, None)
    optind += 1
    command    = list_get(non_opts, optind, None)
    optind += 1

    if target is None :
        logger.debug('DEBUG: target is not defined')
        usage_target(path2cls, mod2ctl)
        sys.exit(1)

    if module is None :
        #module = 'core'
        usage_base(path2cls, mod2ctl)
        sys.exit(1)

    if not module in mod2ctl :
        logger.debug(mod2ctl)
        print('ERROR: no such module, {0}'.format(module))
        usage_base(path2cls, mod2ctl)
        sys.exit(1) 

    if controller is None :
        controller = 'system'
        logger.error("no controller name for module '{0}'".format(module))
        usage_module(module, mod2ctl[module])
        sys.exit(1)
    
    if command is None :
        #command = 'status'
        msg = "no command name for module '{0}', controller '{1}'".format(module, controller)
        logger.error(msg)
        usage_controller(module, controller, path2cls)
        sys.exit(1)
   
    command_aliases = {
        'import' : 'load',
        'export' : 'save',
    }

    command = command_aliases.get(command, command)

    if 'help' in opts:
        usage_command(module, controller, command, path2cls)
        sys.exit(1)
        
 
    key = os.getenv('key')
    if not key :
        print('ERROR: no environment variable, "key"')
        ret = ret + 1
    secret = os.getenv('secret')
    if not secret :
        print('ERROR: no environment variable, "secret"')
        ret = ret + 1
    if ret :
        sys.exit(1)

    base_url = 'https://{0}'.format(target)
    
    logger.debug('OPNsenseClient')

    client = OPNsenseClient(
        base_url=base_url,
        key=key,
        secret=secret,
        verify_ssl=verify_ssl,
    )
  
    logger.debug('module     : {0}'.format(module))
    logger.debug('controller : {0}'.format(controller))
    logger.debug('command    : {0}'.format(command))

    if controller == 'filter' :
        data = {
          'rule' : payload
        }
    else :
        data = {
          controller : payload
        }
    
    logger.debug('Payload: {0}'.format(data))

    modulepath = module + '/' + controller + '.py'

    if not modulepath in path2cls:
        logger.error('NOT found {0} in path2cls'.format(modulepath))
        sys.exit(1)

    logger.debug('found {0} in path2cls'.format(modulepath))
    logger.debug('check {0} in path2cls...'.format(modulepath))
    api_class_name = path2cls[modulepath]
    logger.debug('api_class_name is {0}'.format(api_class_name))

    mod_obj = get_module_object(modulepath)
    logger.debug(mod_obj)
    
    # get class object
    class_obj = get_class_object(mod_obj, api_class_name)
    logger.debug(class_obj)

    # create instance
    instance = create_instance(class_obj, client)

    # get method
    method = get_class_method(instance, command)
    if not method :
        msg = "controller '{0}' DOES NOT have such command, '{1}'".format(controller, command)
        logger.error(msg)
        usage_controller(module, controller, path2cls)
        sys.exit(1)

    res = method(data, params)
    if res :
        fp.write(json.dumps(res, indent=4))
        fp.write('\n')
    
    if output :
        fp.close()

if __name__ == "__main__":
    main()
