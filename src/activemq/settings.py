# ################################################################################# #
# ServiceClients Repository : https://github.com/ISISSoftwareServices/ServiceClients
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# ################################################################################# #
from src.settings import ClientSettings


# pylint:disable=too-few-public-methods
class ActiveMQSettings(ClientSettings):
    """
    ActiveMq settings to be used as a Queue settings object
    """
    all_subscriptions = None

    # pylint:disable=too-many-arguments
    def __init__(self,
                 reduction_pending='/queue/ReductionPending',
                 data_ready='/queue/DataReady',
                 reduction_started='/queue/ReductionStarted',
                 reduction_complete='/queue/ReductionComplete',
                 reduction_error='/queue/ReductionError',
                 reduction_skipped='/queue/ReductionSkipped',
                 **kwargs):
        super(ActiveMQSettings, self).__init__(**kwargs)

        self.reduction_pending = reduction_pending
        self.data_ready = data_ready
        self.reduction_started = reduction_started
        self.reduction_complete = reduction_complete
        self.reduction_error = reduction_error
        self.reduction_skipped = reduction_skipped
        self.all_subscriptions = [data_ready, reduction_started,
                                  reduction_complete, reduction_error, reduction_skipped]