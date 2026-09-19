import sys
import logging
logger = logging.getLogger(__name__)

from opnsense.client import OPNsenseClient


class CoreFirmwareAPI:
    """
    OPNsense Core Firmware API
    module: core
    controller: firmware
    commands: install, remove, reinstall
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client
    
    def __show_options(self):
        print('  OPTIONS:')
        print('    EX. --pkg_name=os-net-snmp')
    
    def __install(self, mod, ctl, cmd):
        self.__show_options()

    def install(self, data=None, params=None):
        """
        Install package
        POST /api/core/firmware/install
        """
        if not 'pkg_name' in params :
            logger.error('no pkg_name param')
            self.__show_options()
            sys.exit(2)
            
        pkg_name = params['pkg_name']
        url = "/api/core/firmware/install/{0}".format(pkg_name)
        return self.client.post(url)

    def __remove(self, mod, ctl, cmd):
        self.__show_options()

    def remove(self, data=None, params=None):
        """
        Remove package
        POST /api/core/firmware/remove
        """
        if not 'pkg_name' in params:
            logger.error('no pkg_name param')
            self.__show_options()
            sys.exit(2)

        pkg_name = params['pkg_name']
        url = "/api/core/firmware/remove/{0}".format(pkg_name)
        return self.client.post(url)

    def __reinstall(self, mod, ctl, cmd):
        self.__show_options()

    def reinstall(self, data=None, params=None):
        """
        Reinstall package
        POST /api/core/firmware/reinstall
        """
        if not 'pkg_name' in params:
            logger.error('no pkg_name param')
            self.__show_options()
            sys.exit(2)
        pkg_name = params['pkg_name']
        url = "/api/core/firmware/reinstall/{0}".format(pkg_name)
        return self.client.post(url)
    
    def __info(self, mod, ctl, cmd):
        print('no options')

    def info(self, data=None, params=None):
        """
        Show firmware information
        GET /api/core/firmware/info
        """
        url = "/api/core/firmware/info"
        return self.client.get(url)

    def __get(self, mod, ctl, cmd):
        print('no options')

    def get(self, data=None, params=None):
        """
        Get firmware information
        GET /api/core/firmware/get
        """
        url = "/api/core/firmware/get"
        return self.client.get(url)

