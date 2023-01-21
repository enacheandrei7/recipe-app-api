"""
Test custom Django management commands
"""
from unittest.mock import patch  # mocks behaviour of db

from psycopg2 import OperationalError as Psycopg2OpError  # possibilities of errors of connecting to db before the db is initialized

from django.core.management import call_command  # simulate/call command by name
from django.db.utils import OperationalError  # exception that may be thrown by database
from django.test import SimpleTestCase  # base test class for testing


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db if db ready"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
                                    [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
