import os
import sys

from pprint import pprint
import subprocess
import shlex

import re

from helpers import check_message

def test_cli():
    cmd = 'opncli'
    args = shlex.split(cmd)
    proc = subprocess.Popen(args,
             stdout=subprocess.PIPE,
             stderr=subprocess.PIPE,
             text=True,
           )

    msg = 'Available Modules:'
    ret = check_message(proc, msg)
    assert ret == 1

def test_cli_core():
    cmd = 'opncli core --help'
    args = shlex.split(cmd)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)

    msg = 'Available Controller for core'
    ret = check_message(proc, msg)
    assert ret == 1

def test_cli_core_system_status():
    cmd = 'opncli core system status'
    args = shlex.split(cmd)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)

    msg = '"dialogTitle": "System Status"'
    ret = check_message(proc, msg)
    assert ret == 0


def test_cli_core_system_status_with_target():
    target = os.getenv("target")
    cmd = 'opncli core system status -t {0}'.format(target)
    args = shlex.split(cmd)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)

    msg = '"dialogTitle": "System Status"'
    ret = check_message(proc, msg)
    assert ret == 0
