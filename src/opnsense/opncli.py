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

from opnsense.interfaces import InterfacesAPI

from opnsense.client import OPNsenseClient
from opnsense.firewall import FirewallAPI
from opnsense.interfaces import InterfacesAPI
from opnsense.interfaces.vip_settings import VipSettingsAPI
from opnsense.firewall.category import CategoryAPI

from opnsense.utils.vip import vip_add, vip_clean, vip_list
from opnsense.utils.rule import rule_add, rule_clean, rule_list
from opnsense.utils.category import category_add, category_clean, category_list

#from opnsense.netsnmp.general import netsnmp_get, netsnmp_set
#from opnsense.netsnmp.service import netsnmp_reconfigure

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import logging
logger = logging.getLogger(__name__)

from pprint import pprint

load_dotenv(dotenv_path="./config.conf")
load_dotenv(dotenv_path=".env")

api_modules = {}
available_controllers = {}

def usage_simple():
    prog = os.path.basename(sys.argv[0])
    print('usage: {0} MODULE CONTROLLER COMMAND [OPTIONS]'.format(prog))
    print('  Available Modules:')
    print('    ', end='')
    for module_name in available_controllers :
        print('{0} '.format(module_name), end='')
    print('')

def usage():
    prog = os.path.basename(sys.argv[0])
    print('usage: {0} MODULE CONTROLLER COMMAND [OPTIONS]'.format(prog))
    print('  Available Module, Controller:')
    for module_name in available_controllers :
        print('    Module: {0}'.format(module_name))
        print('      Controllers: ', end='')
        for controller_name in available_controllers[module_name]:
            print('{0}, '.format(controller_name), end='')
        print('')
        print('')
    print('')


def usage_module(module_name, controllers):
    prog = os.path.basename(sys.argv[0])
    print('usage: {0} MODULE CONTROLLER COMMAND [OPTIONS]'.format(prog))
    print('')

    print('  Available Controller for {0}:'.format(module_name))
    print('    ', end='')
    for controller in controllers :
        print('{0} '.format(controller), end='')
    print('')

def usage_controller(module_name, controller_name, api_modules):
    prog = os.path.basename(sys.argv[0])
    print('usage: {0} MODULE CONTROLLER COMMAND [OPTIONS]'.format(prog))
    print('')
  
    modulepath = module_name + '/' + controller_name + '.py'
    mod_obj = get_module_object(modulepath)
   
    api_class_name = api_modules[modulepath]
    # get class object
    class_obj = get_class_object(mod_obj, api_class_name)
    logger.debug(class_obj)

    # create instance
    instance = create_instance(class_obj, None)

    print('  Available Command for {0}/{1}:'.format(module_name, controller_name))
    print('    ', end='')
    for name, func in inspect.getmembers(instance, inspect.ismethod) :
        if re.search(r'^_', name) :
            continue
        print('{0} '.format(name), end='')
    print('')

def usage_command(mod, ctl, cmd, api_modules):
    prog = os.path.basename(sys.argv[0])
    print('usage: {0} {1} {2} {3} [OPTIONS]'.format(prog, mod, ctl, cmd))
    print('')
    
    modulepath = mod + '/' + ctl + '.py'
    mod_obj = get_module_object(modulepath)
   
    api_class_name = api_modules[modulepath]
    # get class object
    class_obj = get_class_object(mod_obj, api_class_name)
    logger.debug(class_obj)

    # create instance
    instance = create_instance(class_obj, None)
    
    # get help method
    method = get_class_method(instance, '__' + cmd)
    if method :
        res = method(mod, ctl, cmd)
    else :
        print('no help message now')

def read_yaml(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    data = yaml.safe_load(fp)
    fp.close()
    return data

def find_api_classes(base_dir: str):
    classes = {}

    for pyfile in pathlib.Path(base_dir).rglob("*.py"):
        rel = pyfile.relative_to(PACKAGE_ROOT)
        with open(pyfile, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(rel))

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if re.search(r'API$', node.name) :
                    classes[node.name] = str(rel)

    return classes

def find_api_modules(base_dir: str):
    modules = {}

    for pyfile in pathlib.Path(base_dir).rglob("*.py"):
        rel = pyfile.relative_to(PACKAGE_ROOT)
        with open(pyfile, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(rel))

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if re.search(r'API$', node.name) :
                    rel_path = str(rel)
                    modules[rel_path] = node.name

    return modules


def find_controllers(api_modules):
    items = {}

    for module_path in api_modules :
        module_path = module_path.replace('.py', '')
        module_name, controller_name = module_path.split('/')
        if controller_name == '__init__' :
            continue

        if not module_name in items:
            items[module_name] = {}
        items[module_name][controller_name] = 1

    return items

def get_module_object(filepath):
    path = filepath
    path = re.sub(r'\.py$', '', path)
    path = re.sub(r'/', '.', path)
    import_path = "opnsense." + path

    mod_obj = importlib.import_module(import_path)
   
    return mod_obj
    
def get_class_object(mod_obj, class_name) :
    class_obj = getattr(mod_obj, class_name)
    return class_obj
    
def get_class_method(instance, command) :
    method = getattr(instance, command, None)
    return method
    
def create_instance(class_obj, client):
    instance = class_obj(client)
    return instance

def parse_args(args):
    data = {}
    for arg in args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            data[key] = value
    return data

def main() :
    ret = 0
    
    output = None
    verify_ssl = False
    loglevel = 'info'
    show_help = False
    configfile = None

    args = []
    payload = {}
    params = {}
   
    api_modules = find_api_modules(pathlib.Path(__file__).parent)
    logger.info(api_modules)

    available_controllers = find_controllers(api_modules)
    
    i = 1
    while i < len(sys.argv) :
        arg = sys.argv[i]
        
        # --help, -h
        m = re.search(r'^(--help|-h)', arg)
        if m :
          show_help = True
          i += 1
          continue
        
        # --config, -c
        m = re.search(r'^(--config|-c)=([^ ]+)', arg)
        if m :
          configfile = m.group(2)
          continue

        # --output, -o
        m = re.search(r'^(--output|-o)(=([^ ]+))?', arg)
        if m :
          if m.group(3) :
            output = m.group(3)
          else :
            i += 1
            arg = sys.argv[i]
            output = arg

          i += 1
          continue
        
        # --verify-ssl
        m = re.search(r'^(--verify-ssl)(=([^ ]+))?', arg)
        if m :
          if m.group(3) :
            verify_ssl = m.group(3)
          else :
            i += 1
            arg = sys.argv[i]
            verify_ssl = arg
          
          i += 1
          continue
        
        # --uuid
        m = re.search(r'^(--uuid)(=([^ ]+))', arg)
        if m :
          key = 'uuid'
          value = m.group(3)
          params[key] = value
          i += 1
          continue
        
        # --loglevel, -l
        m = re.search(r'^(--loglevel|-l)(=([^ ]+))?', arg)
        if m :
          if m.group(3) :
            loglevel = m.group(3)
          else :
            i += 1
            arg = sys.argv[i]
            loglevel = arg
          
          i += 1
          continue
        
        # any param
        m = re.search(r'^(--([^=]+))(=([^ ]+))', arg)
        if m :
          key   = m.group(2) 
          value = m.group(4)
          params[key] = value
          i += 1
          continue

        # key=value
        m = re.search(r'^([^-][^=]+)=([^ ]+)', arg)
        if m :
          key = m.group(1)
          value = m.group(2)
          payload[key] = value
          i += 1
          continue

        # module or controller or command 
        args.append(arg)
        i += 1
    
    logger.debug('payload is {0}'.format(payload))
    
    if ret != 0:
        sys.exit(1)
    
    if loglevel in ('info'):
        level = logging.INFO
    elif loglevel in ('warn', 'warning') :
        level = logging.WARNING
    elif loglevel in ('debug'):
        print('DEBUG: enable debug')
        level = logging.DEBUG
    elif loglevel in ('error'):
        level = logging.ERROR
    elif loglevel in ('critical'):
        level = logging.CRITICAL
    else :
        print('ERROR: unknown loglevel, {0}'.format(loglevel), file=sys.stderr)
        sys.exit(1)

    logging.basicConfig(level=level)
    
    if len(args) == 0:
        logger.error('no module name')
        usage()
        sys.exit(1)
    
    module     = args[0]
    if len(args) == 1:
        logger.error("no controller name for module '{0}'".format(module))
        controllers = available_controllers[module]
        usage_module(module, controllers)
        sys.exit(1)
    
    controller = args[1]
    if len(args) == 2:
        logger.info("no command name for module '{0}', controller '{1}'".format(module, controller))
        usage_controller(module, controller, api_modules)
        sys.exit(1)
    
    command    = args[2]

    if show_help :
        usage_command(module, controller, command, api_modules)
        sys.exit(1)

    load_dotenv()

    key = os.getenv("OPNSENSE_KEY")
    secret = os.getenv("OPNSENSE_SECRET")
    base_url = os.getenv("OPNSENSE_BASE_URL", "https://localhost:8443")
    
    logger.info('OPNsenseClient')

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
    
    logger.info('Payload: {0}'.format(data))
    logger.info('OPNsenseClient')

    modulepath = module + '/' + controller + '.py'

    if not modulepath in api_modules:
        logger.error('NOT found {0} in api_modules'.format(modulepath))
        sys.exit(1)

    logger.debug('found {0} in api_modules'.format(modulepath))
    print('check {0} in api_modules... '.format(modulepath))
    api_class_name = api_modules[modulepath]
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
        usage_controller(module, controller, api_modules)
        sys.exit(1)

    res = method(data, params)
    if res :
        print(json.dumps(res, indent=4))

if __name__ == "__main__":
    main()
