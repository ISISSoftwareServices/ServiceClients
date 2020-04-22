# ################################################################################# #
# ServiceClients Repository : https://github.com/ISISSoftwareServices/ServiceClients
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# ################################################################################# #
"""
The Settings class containing all the recorded field for an ICAT Cleint
"""
from src.settings import ClientSettings


# pylint:disable=too-few-public-methods
class ICATSettings(ClientSettings):

    auth = None

    def __init__(self, authentication_type='Simple', **kwargs):
        super(ICATSettings, self).__init__(**kwargs)
        self.auth = authentication_type
