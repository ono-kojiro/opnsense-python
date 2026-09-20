from pprint import pprint

def test_core_system_status(core_system_api):
    api = core_system_api
    res = api.status()
    # ex.
    #{
    #    "metadata": {
    #        "system": {
    #            "status": 2,
    #            "message": "No pending messages",
    #            "title": "System"
    #        },
    #        "translations": {
    #            "dialogTitle": "System Status",
    #            "dialogCloseButton": "Close"
    #        },
    #        "subsystems": []
    #    }
    #}
    assert "metadata" in res
    assert "system" in res["metadata"]
    assert "title" in res["metadata"]["system"]

def test_core_menu_tree(core_menu_api):
    api = core_menu_api
    res = api.tree()

    lobby_exists = False
    system_exists = False
    for item in res:
        if 'Id' in item :
            identity = item['Id']
            if identity == 'Lobby' :
                lobby_exists = True
            if identity == 'System' :
                system_exists = True

    #pprint(res)

    assert lobby_exists
    assert system_exists


