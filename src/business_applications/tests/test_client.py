# ################################################################################# #
# ServiceClients Repository : https://github.com/ISISSoftwareServices/ServiceClients
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# ################################################################################# #
"""
Test Cycle ingestion client
"""

from urllib.error import URLError

import unittest

from mock import patch, MagicMock

import suds

from src.business_applications import BusinessApplicationsClient, BusinessApplicationsSettings
from src.connection_exception import ConnectionException


class TestCycleIngestionClient(unittest.TestCase):
    # pylint: disable=protected-access
    """
    Exercises the Cycle ingestion client
    """
    def setUp(self):
        self.valid_value = "valid"
        self.test_credentials =\
            ClientSettingsFactory().create('cycle',
                                           username='valid-user',
                                           password='valid-pass',
                                           host='',
                                           port='',
                                           uows_url='https://api.valid-uows.com/?wsdl',
                                           scheduler_url='https://api.valid-scheduler.com/?wsdl')

    def create_client(self, to_mock=None, credentials=None):
        """ Returns a client with 0 or more mocked instance variables
        :param to_mock: A list of client instance variables to mock
        :param credentials: The credentials to initialise the client with
                            (test credentials used if none supplied)
        :return: A client with 0 or more mocked instance variables """
        if not credentials:
            credentials = self.test_credentials
        client = CycleIngestionClient(credentials)
        if to_mock and "_uows_client" in to_mock:
            client._uows_client = MagicMock()
        if to_mock and "_scheduler_client" in to_mock:
            client._scheduler_client = MagicMock()
        return client

    def test_invalid_init(self):
        """ Test initialisation raises TypeError when given invalid credentials """
        with self.assertRaises(TypeError):
            CycleIngestionClient("invalid")

    def test_default_init(self):
        """ Test initialisation values are set """
        client = CycleIngestionClient()
        self.assertIsNone(client._uows_client)
        self.assertIsNone(client._scheduler_client)
        self.assertIsNone(client._session_id)

    @patch('suds.client.Client.__init__')
    def test_create_uows_client_with_valid_credentials(self, mocked_suds_client):
        """ Test the User Office Web Service client is initialised with the uows_url """
        mocked_suds_client.return_value = None  # Avoids Client.__init__() being called
        client = self.create_client()
        client.create_uows_client()
        mocked_suds_client.assert_called_with(self.test_credentials.uows_url)

    def test_create_uows_client_with_invalid_credentials(self):
        """ Test a URLError is raised if the User Office Web Service client
        is initialised with an invalid uows_url """
        client = CycleIngestionClient()
        client.credentials.uows_url = "https://api.invalid.com/?wsdl"
        with self.assertRaises(URLError):
            client.create_uows_client()

    @patch('suds.client.Client.__init__')
    def test_create_scheduler_client_with_valid_credentials(self, mocked_suds_client):
        """ Test the Scheduler client is initialised with the scheduler_url """
        mocked_suds_client.return_value = None  # Avoids Client.__init__() being called
        client = self.create_client()
        client.create_scheduler_client()
        mocked_suds_client.assert_called_with(self.test_credentials.scheduler_url)

    def test_create_scheduler_client_with_invalid_credentials(self):
        """ Test a URLError is raised if the Scheduler client
        is initialised with an invalid scheduler_url """
        client = CycleIngestionClient()
        client.credentials.scheduler_url = "https://api.invalid.com/?wsdl"
        with self.assertRaises(URLError):
            client.create_scheduler_client()

    def test_connect_with_valid_credentials(self):
        # pylint: disable=line-too-long
        """ Test UOWS login with valid credentials populates _session_id  """
        client = self.create_client(["_uows_client", "_scheduler_client"])
        client._uows_client.service.login.return_value = self.valid_value
        client.connect()
        client._uows_client.service.login.assert_called_with(Account=self.test_credentials.username,
                                                             Password=self.test_credentials.password)
        self.assertEqual(self.valid_value, client._session_id)

    def test_connect_with_invalid_credentials(self):
        # pylint: disable=line-too-long
        """ Test UOWS login with invalid credentials raises a ConnectionException """
        client = self.create_client(["_uows_client"])
        client._uows_client.service.login.side_effect = suds.WebFault(fault=None, document=None)

        with self.assertRaises(ConnectionException):
            client.connect()
        client._uows_client.service.login.assert_called_with(Account=self.test_credentials.username,
                                                             Password=self.test_credentials.password)

    def test_disconnect(self):
        """ Test disconnection from a session sets _session_id = None"""
        client = self.create_client(["_uows_client", "_scheduler_client"])
        client.connect()
        client.disconnect()
        self.assertEqual(None, client._session_id)

    def test_test_connection_no_uows_client(self):
        """ Test the connection test throws the TypeError: "invalid_uows_client"
        When the _uows_client is invalid """
        client = self.create_client(["_uows_client", "_scheduler_client"])
        client.connect()
        client._uows_client = None
        with self.assertRaises(TypeError) as error:
            client._test_connection()
            self.assertEqual(error, client._errors["invalid_uows_client"])

    def test_test_connection_no_scheduler_client(self):
        """ Test the connection test throws the TypeError: "invalid_scheduler_client"
        When the _scheduler_client is invalid """
        client = self.create_client(["_uows_client", "_scheduler_client"])
        client.connect()
        client._scheduler_client = None
        with self.assertRaises(TypeError) as error:
            client._test_connection()
            self.assertEqual(error, client._errors["invalid_scheduler_client"])

    def test_test_connection_no_invalid_session_id(self):
        # pylint: disable=line-too-long
        """ Test the connection test throws the ConnectionException: "invalid_session_id"
        When the _session_id is invalid """
        client = self.create_client(["_uows_client", "_scheduler_client"])
        client._scheduler_client.service.getFacilityList.side_effect = suds.WebFault(fault=None, document=None)
        client.connect()
        client._session_id = None
        with self.assertRaises(ConnectionException) as error:
            client._test_connection()
            self.assertEqual(error, client._errors["invalid_session_id"])

    def test_ingest_cycle_dates(self):
        # pylint: disable=line-too-long
        """ Test the cycle ingestion returns the output received from the Scheduler Client
        and uses the _session_id to do so"""
        client = self.create_client(["_uows_client", "_scheduler_client"])
        client.connect()
        client._scheduler_client.service.getCycles.return_value = self.valid_value
        ret = client.ingest_cycle_dates()
        self.assertEqual(ret, self.valid_value)
        client._scheduler_client.service.getCycles.assert_called_with(sessionId=client._session_id)

    def test_ingest_maintenance_days(self):
        # pylint: disable=line-too-long
        """ Test the maintenance-days ingestion returns the output received
        from the Scheduler Client and uses the _session_id to do so"""
        client = self.create_client(["_uows_client", "_scheduler_client"])
        client.connect()
        client._scheduler_client.service.getOfflinePeriods.return_value = self.valid_value

        ret = client.ingest_maintenance_days()
        self.assertEqual(ret, self.valid_value)
        client._scheduler_client.service.getOfflinePeriods.assert_called_with(sessionId=client._session_id,
                                                                              reason='Maintenance')
