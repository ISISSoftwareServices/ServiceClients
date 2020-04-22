# ################################################################################# #
# ServiceClients Repository : https://github.com/ISISSoftwareServices/ServiceClients
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# ################################################################################# #
from src.settings import ClientSettings


class SFTPSettings(ClientSettings):
    """
    SFTP settings object
    """
    def __init__(self, **kwargs):  # pylint:disable=useless-super-delegation
        super(SFTPSettings, self).__init__(**kwargs)
