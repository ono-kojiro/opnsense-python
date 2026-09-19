#!/usr/bin/env python3

import sys
import os
import re

import logging
logger = logging.getLogger(__name__)

no_argument       = 0
required_argument = 1
optional_argument = 2

__all__ = [
    "init_options",
    "parse_option",
    "no_argument",
    "required_argument",
    "optional_argument",
]

def init_options(long_options):
    opts = {}

    for long_option in long_options :
        opt = long_option[0]
        if opt :
            opts[opt] = None

    return opts

def parse_option(i, args, long_options, opts, params, non_opts):
    arg = args[i]

    name  = None
    value = None

    for l in range(len(long_options)) :
        long_opt  = long_options[l][0]
        has_arg   = long_options[l][1]
        short_opt = long_options[l][3]

        m = re.search(r'^(--{0}|-{1})(=([^ ]+))?'.format(long_opt, short_opt), arg)
        if m :
            name  = long_opt
            value = m.group(3)
            if has_arg and not value :
                i = i + 1
                if i >= len(args) :
                    msg = "option '{0}, {1}' DOES NOT have argument".format(long_opt, short_opt)
                    logger.error(msg)
                    sys.exit(1)
                value = args[i]
            elif not has_arg and value :
                msg = "option '{0}' has argument, '{1}'".format(long_opt, value)
                logger.error(msg)
                sys.exit(1)
            elif not has_arg :
                value = True

            msg = "arg '{0}' matched to {1} option, value is {2}".format(arg, long_opt, value)
            logger.debug(msg)
            opts[name] = value
            break
        else :
            msg = "arg '{0}' not mached to {1} and {2}".format(arg, long_opt, short_opt)
            logger.debug(msg)

    if not name :
        m = re.search(r'^(--([^=]+))(=([^ ]+))?', arg)
        if m :
            name  = m.group(2)
            value = m.group(4)
            msg = "use as parameter, {0}, {1}".format(name, value)
            logger.debug(msg)
            params[name] = value
        else :
            msg = "use as non-optional argument, {0}".format(arg)
            logger.debug(msg)
            non_opts.append(arg)

    return i

