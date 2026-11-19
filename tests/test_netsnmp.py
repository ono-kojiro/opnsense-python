import os
import sys

import pytest
import subprocess
import shlex

import re
import json

from opnsense.client import OPNsenseClient
from opnsense.api.netsnmp.user import UserAPI

from helpers import run_shell, get_categories

def test_netsnmp_user_init():
    cmd = "opncli netsnmp user search_user | jq -r '.rows'"
    
    lines = run_shell(cmd)
    items = json.loads(lines)
    for item in items :
        uuid = item['uuid']
        cmd = f"opncli netsnmp user del_user --uuid={uuid}"
        lines = run_shell(cmd)
        res = json.loads(lines)
        assert res['result'] == 'deleted'

def test_netsnmp_user_get():
    cmd = 'opncli netsnmp user get'
    lines = run_shell(cmd)
    data = json.loads(lines)

    items = data['user']['users']['user']
    assert len(items) == 0

def test_netsnmp_user_add():
    cmd = 'opncli netsnmp user add_user username=myuser password=myauthpass enckey=myprivpass enabled=1'
    
    lines = run_shell(cmd)
    res = json.loads(lines)

    assert res['result'] == 'saved'

def test_netsnmp_user_delete():
    cmd = "opncli netsnmp user search_user | jq -r '.rows'"
    
    lines = run_shell(cmd)
    items = json.loads(lines)
    for item in items :
        uuid = item['uuid']
        cmd = f"opncli netsnmp user del_user --uuid={uuid}"
        lines = run_shell(cmd)
        res = json.loads(lines)
        
        assert res['result'] == 'deleted'


