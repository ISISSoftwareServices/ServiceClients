# ################################################################################# #
# ServiceClients Repository : https://github.com/ISISSoftwareServices/ServiceClients
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# ################################################################################# #
"""
Creates a database session for the reduction database
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, relationship

from src.abstract_client import AbstractClient
from src.connection_exception import ConnectionException


class SQLDatabaseClient(AbstractClient):
    """
    Single access point for the mysql database
    """

    def __init__(self, credentials):
        super(SQLDatabaseClient, self).__init__(credentials)
        self._connection = None
        self._meta_data = None
        self._engine = None

    def connect(self):
        """
        Get the connection to the database service
        :return: The connection to the database
        """
        if self._connection is None:
            connect_string = self.credentials.get_full_connection_string()
            self._engine = create_engine(connect_string, pool_recycle=280)
            self._meta_data = MetaData(self._engine)
            session = sessionmaker(bind=self._engine)
            self._connection = session()
            self._test_connection()
            return self._connection
        return self._connection

    def _test_connection(self):
        """
        Ensure that the connection has been established
        :return: True if connection is establish
        """
        try:
            self._connection.execute('SELECT 1').fetchall()
        # pylint:disable=broad-except
        except Exception as exp:
            # The original exception appears to be wrapped in a different exception
            # as such it is not being consistently caught so we should check
            # the exception name instead
            if type(exp).__name__ == 'OperationalError':
                raise ConnectionException("MySQL")
            raise
        return True

    def get_connection(self):
        """
        Retrieve the session object.
        :return: SQLAlchemy session
        """
        return self._connection

    def disconnect(self):
        """
        Close the connection and reset variables
        """
        self._connection.close()
        self._connection = None
        self._meta_data = None
        self._engine = None

    # ======================== Tables for database access ============================== #
    def instrument(self):
        """
        :return: Instrument Table to replicate what we expect in the database
        """
        # pylint: disable=too-few-public-methods
        class Instrument(declarative_base()):
            """
            Table for reduction_viewer_instrument entity
            """
            __table__ = Table('reduction_viewer_instrument',
                              self._meta_data, autoload=True,
                              autoload_with=self._engine)
        return Instrument

    def reduction_run(self):
        """
        :return: ReductionRun Table to replicate what we expect in the database
        """
        # pylint: disable=too-few-public-methods
        class ReductionRun(declarative_base()):
            """
            Table for reduction_viewer_reductionrun entity
            """
            __table__ = Table('reduction_viewer_reductionrun',
                              self._meta_data, autoload=True,
                              autoload_with=self._engine)
            instrument = relationship(self.instrument(),
                                      foreign_keys='ReductionRun.instrument_id')
            status = relationship(self.status(),
                                  foreign_keys='ReductionRun.status_id')
            experiment = relationship(self.experiment(),
                                      foreign_keys='ReductionRun.experiment_id')
        return ReductionRun

    def reduction_data_location(self):
        """
        :return: ReductionDataLocation Table to replicate what we expect in the database
        """
        # pylint: disable=too-few-public-methods
        class ReductionDataLocation(declarative_base()):
            """
            Table for reduction_viewer_datalocation entity
            """
            __table__ = Table('reduction_viewer_datalocation',
                              self._meta_data, autoload=True,
                              autoload_with=self._engine)
            reduction_run = relationship(self.reduction_run(),
                                         foreign_keys='ReductionDataLocation.reduction_run_id')
        return ReductionDataLocation

    def reduction_location(self):
        """
        :return: ReductionLocation Table to replicate what we expect in the database
        """
        # pylint: disable=too-few-public-methods
        class ReductionLocation(declarative_base()):
            """
            Table for reduction_viewer_reductionlocation entity
            """
            __table__ = Table('reduction_viewer_reductionlocation',
                              self._meta_data, autoload=True,
                              autoload_with=self._engine)
            reduction_run = relationship(self.reduction_run(),
                                         foreign_keys='ReductionLocation.reduction_run_id')
        return ReductionLocation

    def run_variables(self):
        """
        :return: RunVariables Table to replicate what we expect in the database
        """
        # pylint: disable=too-few-public-methods
        class RunVariable(declarative_base()):
            """
            Table for reduction_variables_runvariable entity
            """
            __table__ = Table('reduction_variables_runvariable',
                              self._meta_data, autoload=True,
                              autoload_with=self._engine)
            reduction_run = relationship(self.reduction_run(),
                                         foreign_keys='RunVariable.reduction_run_id')
        return RunVariable

    def experiment(self):
        """
        :return: Experiment Table to replicate what we expect in the database
        """
        # pylint: disable=too-few-public-methods
        class Experiment(declarative_base()):
            """
            Table for reduction_viewer_experiment entity
            """
            __table__ = Table('reduction_viewer_experiment',
                              self._meta_data, autoload=True,
                              autoload_with=self._engine)
        return Experiment

    def status(self):
        """
        :return: Status Table to replicate what we expect in the database
        """
        # pylint: disable=too-few-public-methods
        class Status(declarative_base()):
            """
            Table for reduction_viewer_status entity
            """
            __table__ = Table('reduction_viewer_status',
                              self._meta_data, autoload=True,
                              autoload_with=self._engine)
        return Status
