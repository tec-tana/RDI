class Users:
    def __init__(self):
        self._userinfo = {}
        pass

    def addUser(self, id:str="", token="", *args):
        self._userinfo['name'] = id
        self._userinfo['token'] = token
        self._userinfo['_info'] = (w for w in args)

    def delUser(self):
        try:
            self._userinfo.pop(id)
        except:
            pass    # Here, we can also check token or make sure that
                    # the user exists, why exception is raised, etc.


''' global variables '''

isConnected = False
currentDOI = ""
user = Users()
