"""
Test to test the db connection
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2OperationalError
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test cases for db connection"""

    def test_wait_for_db_ready(self, patch_check):
        """Test waiting for db"""
        patch_check.return_value = True

        call_command('wait_for_db')

        patch_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patch_check):
        """Test waiting for db operational error"""
        patch_check.side_effect = [Psycopg2OperationalError] * 2 + [OperationalError] * 4 + [True]

        call_command('wait_for_db')

        self.assertEqual(patch_check.call_count, 7)

        patch_check.assert_called_with(databases=['default'])
