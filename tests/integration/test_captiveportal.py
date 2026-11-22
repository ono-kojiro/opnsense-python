from pprint import pprint

def test_captiveportal_status(captiveportal_access_api):
    api = captiveportal_access_api
    res = api.status()

    assert res['clientState'] == 'NOT_AUTHORIZED'

def test_captiveportal_service(captiveportal_service_api):
    api = captiveportal_service_api
    res = api.status()

    assert res['status'] == 'disabled'


