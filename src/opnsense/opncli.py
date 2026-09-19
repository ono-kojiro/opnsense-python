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

def usage():
    prog = os.path.basename(sys.argv[0])
    print('usage: {0} MODULE CONTROLLER COMMAND [OPTIONS]'.format(prog))

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
                    modules[str(rel)] = node.name

    return modules

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
    method = getattr(instance, command)
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

    try:
        options, args = getopt.gnu_getopt(
            sys.argv[1:],
            "hvl:",
 #           [
 #             "help",
 #             "version",
 #             "loglevel=",
 #           ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None
    verify_ssl = False
    loglevel = 'info'
    show_help = False

    for option, arg in options:
        if option in ("-v", "-h", "--help"):
            show_help = True
        elif option in ("-o", "--output"):
            output = arg
        elif option in ("--verify-ssl"):
            verify_ssl = bool(arg)
        elif option in ("-l", "--loglevel"):
            loglevel = str(arg)
        else:
            assert False, "unknown option"
    
    for i in range(len(args)):
        print('OPT: args[i] : {0}'.format(args[i]))

    if ret != 0:
        sys.exit(1)
    
    if show_help :
        usage()
        sys.exit(0)

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

    load_dotenv()

    key = os.getenv("OPNSENSE_KEY")
    secret = os.getenv("OPNSENSE_SECRET")
    base_url = os.getenv("OPNSENSE_BASE_URL", "https://localhost:8443")

    client = OPNsenseClient(
        base_url=base_url,
        key=key,
        secret=secret,
        verify_ssl=verify_ssl,
    )

    if len(args) == 0:
        usage()
        sys.exit(1)

    if len(args) < 3:
        usage()
        sys.exit(1)

    module     = args[0]
    controller = args[1]
    command    = args[2]
  
    payload = None
    if len(args) >= 4 :
        payload = parse_args(args[3:])
        print(payload)

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

    api_modules = find_api_modules(pathlib.Path(__file__).parent)
    logger.debug(api_modules)
    modulepath = module + '/' + controller + '.py'

    if not modulepath in api_modules:
        logger.error('NOT found {0} in api_modules'.format(modulepath))
        sys.exit(1)

    logger.debug('found {0} in api_modules'.format(modulepath))
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
    res = method(data)
    print(json.dumps(res, indent=4))

if __name__ == "__main__":
    main()
