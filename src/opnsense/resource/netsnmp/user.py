# src/opnsense/resource/netsnmp/user.py

import logging

from opnsense.api.netsnmp.user import UserAPI

logger = logging.getLogger(__name__)


class User(UserAPI):

    REQUIRED_FIELDS = (
        "username",
        "password",
        "enckey",
        "enabled",
    )

    def _find_uuid(self, username):

        res = self.search_user()

        rows = res.get("rows", [])

        for row in rows:

            if row.get("username") == username:
                return row["uuid"]

        raise ValueError(
            f"user '{username}' not found"
        )

    def _resolve_uuid(self, params):

        if "uuid" in params:
            return params

        if "username" not in params:
            raise ValueError(
                "no uuid parameter and username parameter"
            )

        params = dict(params)

        params["uuid"] = self._find_uuid(
            params["username"]
        )

        return params

    def add_user(self, data):

        user = data.get(
            "user",
            {}
        )

        missing = []

        for field in self.REQUIRED_FIELDS:

            if field not in user:
                missing.append(field)

        if missing:

            raise ValueError(
                "missing fields: "
                + ", ".join(missing)
            )

        return super().add_user(data)

    def get_user(self, params):

        params = self._resolve_uuid(params)

        return super().get_user(params)

    def del_user(self, params):

        params = self._resolve_uuid(params)

        return super().del_user(params)

    def set_user(self, data, params):

        params = self._resolve_uuid(params)

        return super().set_user(
            data,
            params
        )

    def toggle_user(self, params):

        params = self._resolve_uuid(params)

        return super().toggle_user(params)

