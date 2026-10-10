import os
import sys
import re

import importlib
import pathlib
import ast
import inspect

import logging
logger = logging.getLogger(__name__)

from pprint import pprint

__all__ = [
  'usage_target',
  'usage_base',
  'usage_simple',
  'usage_module',
  'usage_controller',
  'usage_command',
  'get_module_object',
  'find_api_modules',
  'find_api_classes',
  'find_controllers',
  'get_class_object',
  'get_class_method',
  'create_instance',
]

def read_yaml(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    data = yaml.safe_load(fp)
    fp.close()
    return data


def find_api_classes(base_dir: str, package_root):
    classes = {}

    for pyfile in pathlib.Path(base_dir).rglob("*.py"):
        rel = pyfile.relative_to(package_root)
        with open(pyfile, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(rel))

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if re.search(r'API$', node.name) :
                    classes[node.name] = str(rel)

    return classes

def find_api_modules(base_dir: str, package_root):
    modules = {}

    for pyfile in pathlib.Path(base_dir).rglob("*.py"):
        rel = pyfile.relative_to(package_root)
        with open(pyfile, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(rel))

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if re.search(r'API$', node.name) :
                    rel_path = str(rel)
                    modules[rel_path] = node.name

    return modules

def get_module_names(api_modules):
    items = {}

    for module_path in api_modules :
        module_path = module_path.replace('.py', '')
        module_name, controller_name = module_path.split('/')
        items[module_name] = 1

    return sorted(list(items))

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

def get_class_object(mod_obj, class_name) :
    class_obj = getattr(mod_obj, class_name)
    return class_obj

def get_class_methods(instance) :
    items = []
    for name, func in inspect.getmembers(instance, inspect.ismethod) :
        if re.search(r'^_', name) :
            continue
        items.append(name)
    return items
    
def get_class_method(instance, command) :
    logger.debug(instance)
    logger.debug("getattr for command {0}".format(command))
    method = getattr(instance, command, None)
    return method
    
def create_instance(class_obj, client):
    instance = class_obj(client)
    return instance


def get_module_object(filepath):
    path = filepath
    path = re.sub(r'\.py$', '', path)
    path = re.sub(r'/', '.', path)
    import_path = "opnsense." + path

    mod_obj = importlib.import_module(import_path)
   
    return mod_obj

def usage_simple(available_controllers):
    prog = os.path.basename(sys.argv[0])

    lines = []
    line = 'usage: {0} MODULE CONTROLLER COMMAND [OPTIONS]'.format(prog)
    lines.append(line)


    lines.append('  Available Modules:')
    line = '    '
    for module_name in available_controllers :
        line = line + '{0} '.format(module_name)
    lines.append(line)

    msg = '''
The module details are displayed when you add the help option to the module.

  ex.
    $ opncli core --help
'''

    lines.append(msg)

    for line in lines:
        print('{0}'.format(line), file=sys.stderr)

def print_available_modules(module_names):
    lines = []

    lines.append('  Available Modules:')
    line = '    '
    for name in module_names:
        line += ' {0},'.format(name)
    line = re.sub(r',$', '', line)
    lines.append(line)
    lines.append('')

    for line in lines:
        print('{0}'.format(line), file=sys.stderr)

def print_available_controllers(module_names, mod2ctl):
    lines = []

    lines.append('  Available Controllers:')
    for name in module_names:
        line = '    {0}:'.format(name)
        controllers = mod2ctl[name]
        for cont in controllers:
            line = line + ' {0},'.format(cont)
        line = re.sub(r',$', '', line)
        lines.append(line)
    lines.append('')
    
    for line in lines:
        print('{0}'.format(line), file=sys.stderr)

def usage_base(api_modules, mod2ctl) :
    module_names = get_module_names(api_modules)

    prog = os.path.basename(sys.argv[0])

    lines = []
    line = 'usage: {0} '.format(prog)
    line = line + 'TARGET MODULE CONTROLLER COMMAND [OPTIONS]'
    lines.append(line)

    msg = '''
  TARGET:  IP address of target OPNsense
  MODULE:  core, interfaces, firewall and so on...
  CONTROLLERS: system(for core), settings(for interfaces) and so on...
  COMMAND: get, set and so on (depend on MODULE)
'''
    lines.append(msg)
    
    for line in lines:
        print('{0}'.format(line), file=sys.stderr)

    print_available_modules(module_names)
    print_available_controllers(module_names, mod2ctl)

    msg = '''
  Environment Variables:
    key:    OPNsense API Key
    secret: OPNsense Secret
'''
    print(msg, file=sys.stderr)

def usage_target(modpath2cls, mod2ctl):
    usage_base(modpath2cls, mod2ctl)
    sys.exit(1)

def usage_module(module_name, controllers):

    print('  Available Controller for {0}:'.format(module_name), file=sys.stderr)
    print('    ', end='', file=sys.stderr)
    for controller in controllers :
        print('{0} '.format(controller), end='', file=sys.stderr)
    print('', file=sys.stderr)
    
    msg = '''
The controller details are displayed when you add the help option to the controller.

  ex.
    $ opncli core system --help
'''

    print(msg, file=sys.stderr)

def usage_controller(module_name, controller_name, api_modules):
    lines = []

    modulepath = module_name + '/' + controller_name + '.py'
    mod_obj = get_module_object(modulepath)
  
    api_class_name = api_modules[modulepath]
    # get class object
    class_obj = get_class_object(mod_obj, api_class_name)
    logger.debug(class_obj)

    # create instance
    instance = create_instance(class_obj, None)

    line = '  Available Command for {0}/{1}:'.format(module_name, controller_name)
    lines.append(line)
    line = '    '

    methods = get_class_methods(instance)

    for name in methods :
        line = line + '{0} '.format(name)
    lines.append(line)

    for line in lines:
        print('{0}'.format(line), file=sys.stderr)

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
    
    logger.debug(instance)
    
    # get help method
    method_name = '_' + api_class_name + '__' + cmd
    logger.debug("check method name '{0}' ...".format(method_name))
    method = get_class_method(instance, method_name)
    if method :
        logger.debug('method is {0}'.format(method))
        logger.debug('call help message')
        res = method(mod, ctl, cmd)
    else :
        logger.info('no help message now')

