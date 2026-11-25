# src/opnsense/opncli/discovery.py

import pathlib
import ast
import re

import logging
logger = logging.getLogger(__name__)

__all__ = [
    'find_api_classes',
    'find_api_modules',
    'find_controllers',
    'get_module_names',
]

def find_api_classes(base_dir, package_root):
    classes = {}

    for pyfile in pathlib.Path(base_dir).rglob("*.py"):
        rel = pyfile.relative_to(package_root)

        with open(pyfile, "r", encoding="utf-8") as fp:
            tree = ast.parse(fp.read(), filename=str(rel))

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if re.search(r'API$', node.name):
                    classes[node.name] = str(rel)

    return classes


def find_api_modules(base_dir, package_root):
    modules = {}

    for pyfile in pathlib.Path(base_dir).rglob("*.py"):
        rel = pyfile.relative_to(package_root)

        with open(pyfile, "r", encoding="utf-8") as fp:
            tree = ast.parse(fp.read(), filename=str(rel))

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if re.search(r'API$', node.name):

                    rel_path = str(rel)

                    #
                    # api/core/system.py
                    # ↓
                    # core/system.py
                    #
                    if rel_path.startswith('api/'):
                        rel_path = rel_path[4:]

                    modules[rel_path] = node.name

    return modules


def get_module_names(api_modules):
    items = {}

    for module_path in api_modules:
        module_path = module_path.replace('.py', '')

        parts = module_path.split('/')

        module_name = parts[-2]

        items[module_name] = 1

    return sorted(items.keys())

def find_controllers(api_modules):
    items = {}

    for module_path in api_modules:
        module_path = module_path.replace('.py', '')

        parts = module_path.split('/')

        #
        # api/core/system
        # -> core, system
        #
        module_name = parts[-2]
        controller_name = parts[-1]

        if controller_name == '__init__':
            continue

        if module_name not in items:
            items[module_name] = {}

        items[module_name][controller_name] = 1

    return items
