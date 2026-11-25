# src/opnsense/opncli/reflection.py

import inspect
import importlib
import re

import logging
logger = logging.getLogger(__name__)

__all__ = [
    'get_module_object',
    'get_controller_class',
    'get_class_object',
    'create_instance',
    'get_class_methods',
    'get_class_method',
]


def get_module_object(filepath):
    path = filepath

    path = re.sub(r'\.py$', '', path)
    path = re.sub(r'/', '.', path)

    #
    # Resource優先
    #
    for base in (
        "opnsense.resource",
        "opnsense.api",
    ):
        import_path = f"{base}.{path}"

        try:
            logger.debug(
                "try import module %s",
                import_path
            )

            return importlib.import_module(import_path)

        except ModuleNotFoundError:
            pass

    raise ModuleNotFoundError(filepath)


def get_controller_class(mod_obj):
    """
    Resourceクラスを優先する。

    例:

        Category
        Alias

    Resourceが無ければ

        CategoryAPI
        AliasAPI

    を返す。
    """

    resource_class = None
    api_class = None

    for _, obj in inspect.getmembers(
        mod_obj,
        inspect.isclass,
    ):

        #
        # importされた他モジュールのクラス除外
        #
        if obj.__module__ != mod_obj.__name__:
            continue

        if obj.__name__.endswith("API"):
            api_class = obj
        else:
            resource_class = obj

    if resource_class:
        logger.debug(
            "use resource class %s",
            resource_class.__name__,
        )
        return resource_class

    if api_class:
        logger.debug(
            "use api class %s",
            api_class.__name__,
        )
        return api_class

    raise RuntimeError(
        f"controller class not found in "
        f"{mod_obj.__name__}"
    )


def get_class_object(mod_obj, class_name):
    return getattr(mod_obj, class_name)


def create_instance(class_obj, client):
    return class_obj(client)


def get_class_methods(instance):
    items = []

    for name, func in inspect.getmembers(
        instance,
        inspect.ismethod
    ):
        if name.startswith('_'):
            continue

        items.append(name)

    return items


def get_class_method(instance, command):
    return getattr(instance, command, None)
