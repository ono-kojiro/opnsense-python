import os
import pytest

from dotenv import load_dotenv

from opnsense.client import OPNsenseClient

from opnsense.auth.group import AuthGroupAPI

from opnsense.core.system import CoreSystemAPI
from opnsense.core.menu   import CoreMenuAPI

from opnsense.firewall import FirewallAPI
from opnsense.interfaces import InterfacesAPI

# プロジェクトルートの .env を読み込む
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

@pytest.fixture(scope="session")
def opnsense_credentials():
    key = os.getenv("OPNSENSE_KEY")
    secret = os.getenv("OPNSENSE_SECRET")
    base_url = os.getenv("OPNSENSE_BASE_URL", "https://localhost:8443")

    if not key or not secret:
        raise RuntimeError("OPNSENSE_KEY / OPNSENSE_SECRET が .env に設定されていません")

    return {
        "key": key,
        "secret": secret,
        "base_url": base_url,
    }

@pytest.fixture
def opnsense_client(opnsense_credentials):
    return OPNsenseClient(
        base_url=opnsense_credentials["base_url"],
        key=opnsense_credentials["key"],
        secret=opnsense_credentials["secret"],
        verify_ssl=False,
    )

#
# Module: Auth
# 
@pytest.fixture
def auth_group_api(opnsense_client):
    return AuthGroupAPI(opnsense_client)

#
# Module: Core
#
@pytest.fixture
def core_system_api(opnsense_client):
    return CoreSystemAPI(opnsense_client)

@pytest.fixture
def core_menu_api(opnsense_client):
    return CoreMenuAPI(opnsense_client)

#
# Module: Firewall
#
@pytest.fixture
def firewall_api(opnsense_client):
    return FirewallAPI(opnsense_client)

#
# Module: Interfaces
#
@pytest.fixture
def interfaces_api(opnsense_client):
    return InterfacesAPI(opnsense_client)

