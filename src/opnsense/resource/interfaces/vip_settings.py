# src/opnsense/resource/interfaces/vip_settings.py

import logging

from opnsense.api.interfaces.vip_settings import VipSettingsAPI

logger = logging.getLogger(__name__)


class VipSettings(VipSettingsAPI):

    def _find_uuid(self, descr):
        res = self.get()

        items = res['vip']['vip']

        for uuid in items:
            item = items[uuid]

            if item.get('descr') == descr:
                return uuid

        raise ValueError(
            f'vip "{descr}" not found'
        )

    #
    # aliases
    #

    def add(self, data):
        return self.add_item(data)

    def delete(self, params):
        return self.del_item(params)

    #
    # extended methods
    #

    def del_item(self, params):

        if 'uuid' not in params:

            if 'descr' not in params:
                raise ValueError(
                    'no uuid/descr parameter'
                )

            params = dict(params)

            params['uuid'] = self._find_uuid(
                params['descr']
            )

        return super().del_item(params)

    def get_item(self, params):

        if 'uuid' not in params:

            if 'descr' not in params:
                raise ValueError(
                    'no uuid/descr parameter'
                )

            params = dict(params)

            params['uuid'] = self._find_uuid(
                params['descr']
            )

        return super().get_item(params)

    def set_item(self, data, params):

        if 'uuid' not in params:

            if 'descr' not in params:
                raise ValueError(
                    'no uuid/descr parameter'
                )

            params = dict(params)

            params['uuid'] = self._find_uuid(
                params['descr']
            )

        return super().set_item(data, params)

