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
        self._userinfo['coll'] = MessageToDict(datafed.command('ls')[0])  # Listing all files in root folder
        #TODO: review this. There should be a better implementation for such a common task i.e. filtering out dict keys.
        # 10-29-2019: ok using filter is the way to go lol
        _listing = self._userinfo['coll']['item']
        self._userinfo['coll']['item'] = list(filter(lambda item: item['id'][0] is 'c', _listing))

    #TODO: heirachy of Collection and Project + the requirement in registering a file has to be reviewed
    # Right now, heirachy is not exerted. Also, if Qcombobox is -1 if not selected, is this what makes nd<0?
    # If that is the case, we still have to raise error instead of return None. The exception should be handled
    # by the user function.
    def list_project_id(self, nd=None):
        ''' project: return a list of item IDs '''
        if nd is -1: return None  # Qcombobox is -1 if not selected
        try:
            projects = self._userinfo['project']['item']
            id_list = [item['id'] for item in projects]
            if nd:
                return id_list[nd]
            return id_list
        except:  # if no project exist
            return None

    def list_project_title(self, nd=None):
        ''' project: return a list of item titles '''
        if nd is -1: return None  # Qcombobox is -1 if not selected
        try:
            projects = self._userinfo['project']['item']
            title_list = [item['title'] for item in projects]
            if nd:
                return title_list[nd]
            return title_list
        except:  # if no project exist
            return None

    def list_coll_id(self, nd=None):
        ''' collection: return a list of item IDs '''
        if nd is -1: return None  # Qcombobox is -1 if not selected
        try:
            collections = self._userinfo['coll']['item']
            id_list = [item['id'] for item in collections]
            if nd:
                return id_list[nd]
            return id_list
        except:  # if no collection exist
            return None

    def list_coll_title(self, nd=None):
        ''' collection: return a list of item titles '''
        if nd is -1: return None  # Qcombobox is -1 if not selected
        try:
            collections = self._userinfo['coll']['item']
            title_list = [item['title'] for item in collections]
            if nd:
                return title_list[nd]
            return title_list
        except:  # if no collection exist
            return None

    def add_coll(self, title:str, alias:str="", coll:str="", project:str="", dcrpt:str=""):
        """
        add new collection to project & register on DataFed
        TODO: add other optional fields as well
        """
        prefix = [' -a ', ' -p ', ' -c ', ' -d ']
        input = [alias, coll, project, dcrpt]
        print(input)
        cmd = ''
        for k, w in enumerate(input):
            if w is not '' and isinstance(w, str):
                cmd += prefix[k]+"\""+w+"\""
        print(cmd)
        datafed.command('data create '+title+cmd)

class DOI_manager:
    """
    This class stores configurations for DOI that is currently working on.
    It should automatically sync with DataFed while storing locally for processes.
    """
    def __init__(self, user):
        self.user = user

    def apply_template(self):
        pass

    def save_setting(self):
        pass

    def update_doi(self, id:str):
        ''' list DOI in a given collection / projects '''
        from google.protobuf.json_format import MessageToDict
        if id[:2] == 'c/' or id[:2] == 'p/':
            try:
                self.user._userinfo['doi'] = MessageToDict(datafed.command('ls '+str(id))[0])
                #print(self.user._userinfo['doi'])
            except Exception as e:  # invalid or non-existing records will yield "ID_BAD_REQUEST"
                self.user._userinfo['doi'] = {}  # give blank
        else:
            raise ValueError("ID given is neither a collection (c/) or a project (p/)")

    def list_doi_id(self):
        try:
            return [item['id'] for item in self.user._userinfo['doi']['item']]
        except:
            return None

    def list_doi_title(self):
        try:
            return [item['title'] for item in self.user._userinfo['doi']['item']]
        except:
            return None

