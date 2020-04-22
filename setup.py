# ################################################################################# #
# ServiceClients Repository : https://github.com/ISISSoftwareServices/ServiceClients
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# ################################################################################# #
# pylint:skip-file
from setuptools import setup


setup_requires = ['mysqlclient',
                  'mysql-connector',
                  'PyMySQL',
                  'pysftp',
                  'SQLAlchemy',
                  'stomp.py',
                  'suds-py3']


setup(name='ServiceClients',
      version='0.1',
      description='A collection of Client classes for accessing services',
      author='ISIS Scientific software Group',
      url='https://github.com/ISISSoftwareServices/ServiceClients',
      install_requires=setup_requires,
     )
