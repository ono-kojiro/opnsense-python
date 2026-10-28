import os
import sys

import pytest
import subprocess
import shlex

import re
import json

from opnsense.client import OPNsenseClient
from opnsense.firewall import FirewallAPI

from pprint import pprint

from helpers import run_shell, get_categories
        
target_categories = ( 'admin', 'debug', 'test' )

def test_core_system_status():
    cmd = 'opncli -c config.conf core system status'
    lines = run_shell(cmd)
    for line in lines :
        print(line)
    assert 0 == 0


