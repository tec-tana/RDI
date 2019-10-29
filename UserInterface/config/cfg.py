from admin import datafedUtility as util

''' global variables '''

dev_user = ('techtana', 'Tech@6684')

isConnected = False  # this is connecting between login dialog and main window
currentDOI = ""  # identity of current data set to work on
user = util.User()
experiment = util.DOI_manager(user)
