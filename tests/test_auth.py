from pprint import pprint

def test_auth_group_search(auth_group_api):
    api = auth_group_api
    res = api.search()

    admins_exists = False

    for row in res["rows"] :
        if row['name'] == 'admins' :
            admins_exists = True

    assert admins_exists

