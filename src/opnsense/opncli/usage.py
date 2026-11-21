# src/opnsense/opncli/usage.py

import os
import sys
import re

import logging
logger = logging.getLogger(__name__)

from opnsense.opncli.discovery import (
    get_module_names,
)

from opnsense.opncli.reflection import (
    get_module_object,
    get_controller_class,
    create_instance,
    get_class_methods,
    get_class_method,
)

__all__ = [
    'usage_target',
    'usage_base',
    'usage_simple',
    'usage_module',
    'usage_controller',
    'usage_command',
]


def usage_simple(available_controllers):
    prog = os.path.basename(sys.argv[0])

    lines = []

    line = (
        f'usage: {prog} '
        'MODULE CONTROLLER COMMAND [OPTIONS]'
    )
    lines.append(line)

    lines.append('  Available Modules:')

    line = '    '
    for module_name in available_controllers:
        line += f'{module_name} '
    lines.append(line)

    msg = '''
The module details are displayed when you add the help option to the module.

  ex.
    $ opncli core --help
'''
    lines.append(msg)

    for line in lines:
        print(line, file=sys.stderr)


def print_available_modules(module_names):
    lines = []

    lines.append('  Available Modules:')

    line = '    '
    for name in module_names:
        line += f' {name},'

    line = re.sub(r',$', '', line)
    lines.append(line)
    lines.append('')

    for line in lines:
        print(line, file=sys.stderr)


def print_available_controllers(module_names, mod2ctl):
    lines = []

    lines.append('  Available Controllers:')

    for name in module_names:
        line = f'    {name}:'

        controllers = mod2ctl[name]

        for cont in controllers:
            line += f' {cont},'

        line = re.sub(r',$', '', line)

        lines.append(line)

    lines.append('')

    for line in lines:
        print(line, file=sys.stderr)


def usage_base(api_modules, mod2ctl):

    module_names = get_module_names(api_modules)

    prog = os.path.basename(sys.argv[0])

    lines = []

    line = (
        f'usage: {prog} '
        'MODULE CONTROLLER COMMAND [OPTIONS]'
    )
    lines.append(line)

    msg = '''
  MODULE:  core, interfaces, firewall and so on...
  CONTROLLERS: system(for core), settings(for interfaces) and so on...
  COMMAND: get, set and so on (depend on MODULE)
'''
    lines.append(msg)

    msg = '''
    -t, --target TARGET       IP address of target OPNsense
    -c, --config CONFIG       configuration file including key and secret
    -l, --loglevel LEVEL      log level, debug, info and so on...
'''
    lines.append(msg)

    for line in lines:
        print(line, file=sys.stderr)

    print_available_modules(module_names)

    msg = '''
  Environment Variables:
    key:    OPNsense API Key
    secret: OPNsense Secret
'''
    print(msg, file=sys.stderr)

    msg = '''
  Examples:
    $ opncli 192.168.122.10 core system status
'''
    print(msg, file=sys.stderr)


def usage_target(modpath2cls, mod2ctl):
    usage_base(modpath2cls, mod2ctl)
    sys.exit(1)


def usage_module(module_name, controllers):

    print(
        f'  Available Controller for {module_name}:',
        file=sys.stderr
    )

    print('    ', end='', file=sys.stderr)

    for controller in controllers:
        print(
            f'{controller} ',
            end='',
            file=sys.stderr
        )

    print('', file=sys.stderr)

    msg = '''
The controller details are displayed when you add the help option to the controller.

  ex.
    $ opncli core system --help
'''

    print(msg, file=sys.stderr)


def usage_controller(
    module_name,
    controller_name,
    api_modules,
):
    lines = []

    modulepath = (
        module_name +
        '/' +
        controller_name +
        '.py'
    )

    mod_obj = get_module_object(modulepath)

    class_obj = get_controller_class(mod_obj)

    instance = create_instance(
        class_obj,
        None
    )

    line = (
        f'  Available Command for '
        f'{module_name}/{controller_name}:'
    )
    lines.append(line)

    line = '    '

    methods = get_class_methods(instance)

    for name in methods:
        line += f'{name} '

    lines.append(line)

    for line in lines:
        print(line, file=sys.stderr)


def usage_command(
    mod,
    ctl,
    cmd,
    api_modules,
):
    prog = os.path.basename(sys.argv[0])

    print(
        f'usage: {prog} {mod} {ctl} {cmd} [OPTIONS]'
    )
    print('')

    modulepath = f'{mod}/{ctl}.py'

    mod_obj = get_module_object(modulepath)

    class_obj = get_controller_class(mod_obj)

    instance = create_instance(
        class_obj,
        None
    )

    logger.debug(instance)

    method_name = (
        '_'
        + class_obj.__name__
        + '__'
        + cmd
    )

    logger.debug(
        "check method name '%s' ...",
        method_name
    )

    method = get_class_method(
        instance,
        method_name
    )

    if method:
        logger.debug(
            'call help message'
        )
        method(mod, ctl, cmd)
    else:
        logger.info(
            'no help message now'
        )