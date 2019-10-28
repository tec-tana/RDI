import datafed.CommandLib as datafed


class User:
    """
    This class stores key information about the user logged into the system.
    """
    def __init__(self):
        self._userinfo = {}
        pass

    def addUser(self, id:str="", token="", *args):
        self._userinfo['name'] = id
        self._userinfo['token'] = token
        self._userinfo['_info'] = (w for w in args)

    def delUser(self):  # we're probably never going to delete a user, cuz it's a 1-on-1 operation
        try:
            self._userinfo.pop(id)
        except:
            pass    # Here, we can also check token or make sure that
                    # the user exists, why exception is raised, etc.

    def update_ownership(self):
        # reply from datafed is protobuf, have to convert to dict
        from google.protobuf.json_format import MessageToDict
        self._userinfo['project'] = MessageToDict(datafed.command('project list')[0])  # List all projects
        self._userinfo['coll'] = MessageToDict(datafed.command('ls')[0])  # Listing all collections

    def add_coll(self, id, alias, project):
        """
        add new collection to project & register on DataFed

        :param id:
        :param alias:
        :param project:
        """
        #TODO: Check this command if it's correct
        datafed.command('coll create '+str(alias)+' -p '+str(project))


class DOI_manager:
    """
    This class stores configurations for DOI that is currently working on.
    It should automatically sync with DataFed while storing locally for processes.
    """
    def __init__(self):
        pass

    def apply_template(self):
        pass

    def save_setting(self):
        pass

''' global variables '''

isConnected = False  # this is connecting between login dialog and main window
currentDOI = ""  # identity of current data set to work on
user = User()
doi = DOI_manager()
