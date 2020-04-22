# ################################################################################# #
# ServiceClients Repository : https://github.com/ISISSoftwareServices/ServiceClients
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# ################################################################################# #
"""
Client class for retrieving files via SFTP from servers (e.g. CEPH)
"""
import os.path
import pysftp

from src.abstract_client import AbstractClient
from src.connection_exception import ConnectionException


class SFTPClient(AbstractClient):
    """
    This class allows files to be retrieved from SFTP servers
    """
    def __init__(self, credentials):
        super(SFTPClient, self).__init__(credentials)
        self._connection = None

    def connect(self):
        """
        Create the connection to the SFTP server
        :return: The connection object
        """
        if self._connection is None:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            self._connection = pysftp.Connection(host=self.credentials.host,
                                                 username=self.credentials.username,
                                                 password=self.credentials.password,
                                                 port=int(self.credentials.port),
                                                 cnopts=cnopts)
        self._test_connection()

        return self._connection

    def disconnect(self):
        """
        Disconnect from the SFTP server
        """
        if self._connection is not None:
            self._connection.close()
        self._connection = None

    def _test_connection(self):
        """
        Test whether there is a connection to the SFTP server
        :return: True if there is a connection.
        :raises ConnectionException: If there is no existing connection or it is not valid.
        """

        try:
            self._connection.pwd
        except AttributeError:
            raise ConnectionException("SFTP")
        return True

    def retrieve(self, server_path, local_path=None, override=True):
        """
        Retrieves file from the given server_path and downloads it to the given local_path
        :param server_path: The location of the file on the SFTP server.
        :param local_path:
            The location to download the file to, including filename with extension.
            If None, local_path is the local directory.
        :param override: If True and local_path points to an existing file, will override this file.
        :raises RuntimeError: If any of the following occur:
            1) The server_path does not exist on the SFTP server
            2) The local_path directory does not exist
            3) The local_path points to a directory instead of a file
            4) The local_path points to an existing file, and override is false
            Note: an error message will describe which of the 4 cases above has occurred.
        """

        if self._connection is None:
            self.connect()

        if not self._connection.exists(server_path):
            raise RuntimeError("The server_path does not point to a file. "
                               "Please provide a server_path which points to a file.")

        if local_path is None:
            local_path = ""

        if not override and os.path.isfile(local_path):
            raise RuntimeError("The local_path points to a file which already exists. "
                               "Please provide a different filename in the local_path, "
                               "or set the override flag to True.")

        try:
            self._connection.get(server_path, local_path)
        except FileNotFoundError:
            raise RuntimeError("The local_path does not exist.")
        except PermissionError:
            raise RuntimeError("The local_path is a directory. "
                               "Please ensure the local_path includes a full filename.")
