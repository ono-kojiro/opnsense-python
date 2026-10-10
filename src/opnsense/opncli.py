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

    args = []
    payload = {}
    params = {}
  
    long_options = [
        [ "help",   no_argument,       0, "h" ],
        [ "output", required_argument, 0, "o" ],
        [ "verify-ssl", required_argument, 0, None ],
        [ "loglevel",   required_argument, 0, "l" ],
        [ None, 0, 0, None ],
    ]

    mod2ctl = {}

    path2cls = find_api_modules(pathlib.Path(__file__).parent, PACKAGE_ROOT)
    logger.info(path2cls)

    mod2ctl = find_controllers(path2cls)

    opts = {}
    params = {}
    data = {}
    non_opts = []

    i = 1
    while i < len(sys.argv) :
        i = parse_option(i, sys.argv, long_options, opts, params, data, non_opts)
        i = i + 1

    payload = data
    logger.debug('payload is {0}'.format(payload))
    
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

    target     = list_get(non_opts, 0, None)
    module     = list_get(non_opts, 1, None)
    controller = list_get(non_opts, 2, None)
    command    = list_get(non_opts, 3, None)

    if target is None :
        usage_target(path2cls, mod2ctl)
        sys.exit(1)

    if module is None :
        #module = 'core'
        usage_base(path2cls, mod2ctl)
        sys.exit(1)

    if not module in mod2ctl :
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
