# ################################################################################# #
# ServiceClients Repository : https://github.com/ISISSoftwareServices/ServiceClients
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# ################################################################################# #
from src.settings import ClientSettings


# pylint:disable=too-few-public-methods
class SQLSettings(ClientSettings):
    """
    MySQL settings to be used as a Database settings object
    """
    database = None

    def __init__(self, database_name='autoreduction', **kwargs):
        super(SQLSettings, self).__init__(**kwargs)
        self.database = database_name

    def get_full_connection_string(self):
        """ :return: string for connecting directly to mysql service with user + pass """
        return 'mysql+mysqldb://{0}:{1}@{2}/{3}'.format(self.username,
                                                        self.password,
                                                        self.host,
                                                        self.database)
