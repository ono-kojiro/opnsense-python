from opnsense.client import OPNsenseClient

class CaptiveportalAccessAPI:
    """
    OPNsense Captiveportal Access API
    module: captiveportal
    controller: access
    commands: api, logoff, logon, status
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def status(self, data=None, params=None):
        """
        GET,POST /api/captiveportal/access/status
        """
        return self.client.get("/api/captiveportal/access/status")

