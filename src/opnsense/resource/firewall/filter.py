# src/opnsense/resource/firewall/filter.py

import logging

from opnsense.api.firewall.filter import FilterAPI
from opnsense.resource.firewall.category import Category

logger = logging.getLogger(__name__)


class Filter(FilterAPI):

    def _find_uuid(self, descr):

        res = self.search_rule()

        for row in res['rows']:
            if row.get('description') == descr:
                return row.get('uuid')

        raise ValueError(
            f'rule "{descr}" not found'
        )

    def _convert_categories(self, data):

        rule = data.get('rule', {})

        categories = rule.get('categories')

        if not categories:
            return data

        category_api = Category(self.client)

        res = category_api.get()

        cat_uuids = (
            res['category']
               ['categories']
               ['category']
        )

        cat2uuid = {}

        for uuid in cat_uuids:
            name = cat_uuids[uuid]['name']
            cat2uuid[name] = uuid

        values = []

        for token in categories.split(','):

            token = token.strip()

            uuid = cat2uuid.get(token)

            if uuid is None:
                raise ValueError(
                    f'category "{token}" not found'
                )

            values.append(uuid)

        rule['categories'] = ",".join(values)

        return data

    def add(self, data):
        return self.add_rule(data)

    def delete(self, params):
        return self.del_rule(params)

    def add_rule(self, data):

        data = self._convert_categories(data)

        descr = data['rule']['description']

        res = self.search_rule()

        for row in res['rows']:
            if row['description'] == descr:
                raise ValueError(
                    f'rule "{descr}" already exists'
                )

        return super().add_rule(data)

    def get_rule(self, params):

        if 'uuid' not in params:

            if 'descr' not in params:
                raise ValueError(
                    'no uuid/descr parameter'
                )

            params = dict(params)

            params['uuid'] = self._find_uuid(
                params['descr']
            )

        return super().get_rule(params)

    def set_rule(self, data, params):

        if 'uuid' not in params:

            if 'descr' not in params:
                raise ValueError(
                    'no uuid/descr parameter'
                )

            params = dict(params)

            params['uuid'] = self._find_uuid(
                params['descr']
            )

        data = self._convert_categories(data)

        return super().set_rule(data, params)

    def del_rule(self, params):

        if 'uuid' not in params:

            if 'descr' not in params:
                raise ValueError(
                    'no uuid/descr parameter'
                )

            params = dict(params)

            params['uuid'] = self._find_uuid(
                params['descr']
            )

        return super().del_rule(params)

