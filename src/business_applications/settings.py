# ################################################################################# #
# ServiceClients Repository : https://github.com/ISISSoftwareServices/ServiceClients
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# ################################################################################# #
from src.settings import ClientSettings


class BusinessApplicationsSettings(ClientSettings):
    """
    Cycle-ingestion settings object
    """
    uows_url = None
    scheduler_url = None

    def __init__(self, uows_url, scheduler_url, **kwargs):
        super(BusinessApplicationsSettings, self).__init__(**kwargs)
        self.uows_url = uows_url
        self.scheduler_url = scheduler_url
