# ################################################################################# #
# ServiceClients Repository : https://github.com/ISISSoftwareServices/ServiceClients
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# ################################################################################# #
"""
Custom class for connection errors
"""


class ConnectionException(Exception):
    """
    Simple class for raising exceptions when we cannot connect to services
    """

    def __init__(self, service_name):
        message = "Unable to connect to {0} with provided credentials. " \
                  "Please check the {0} settings files then try again.".format(service_name)
        super(ConnectionException, self).__init__(message)
