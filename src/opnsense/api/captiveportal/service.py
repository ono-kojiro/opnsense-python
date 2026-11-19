from opnsense.client import OPNsenseClient

class CaptiveportalServiceAPI:
    """
    OPNsense Captiveportal Service API
    module: captiveportal
    controller: service
    commands: del_template, get_template, reconfigure, restart
       save_template, search_templates, start, status, stop
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def status(self, data=None, params=None):
        return self.client.get("/api/captiveportal/service/status")

