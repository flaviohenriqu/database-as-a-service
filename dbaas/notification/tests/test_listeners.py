# coding: utf-8
from datetime import datetime
from mock import patch
from unittest import TestCase
from notification.models import save_task, TaskHistory
from notification.tests.factory import TaskHistoryFactory


@patch('notification.models.get_redis_connection')
class SaveTaskTestCase(TestCase):

    def setUp(self):
        self.fake_task = TaskHistoryFactory.build()
        self.fake_task.user = 'admin'

    def _simulate_signal(self):
        save_task(sender=TaskHistory, instance=self.fake_task)

    def test_dont_save_when_no_user(self, mock_conn):
        # mock_conn = MagicMock()
        self.fake_task.user = None
        self._simulate_signal()

        self.assertFalse(mock_conn.hgetall.called)
        self.assertFalse(mock_conn.hmset.called)
        self.assertFalse(mock_conn.expire.called)

    def test_validate_params(self, mock_conn):
        # TODO: Verify why i must do that to work
        mock_conn = mock_conn()
        self.fake_task.task_name = 'notification.fake.fake_task'
        self.fake_task.id = 123
        self.fake_task.task_status = 'SUCCESS'
        self.fake_task.updated_at = datetime(2017, 7, 27, 14, 39, 22, 160307)
        self.fake_task.arguments = 'Database: database_fake, New Disk Offering: Micro'

        self._simulate_signal()

        self.assertTrue(mock_conn.hgetall.called)
        args = mock_conn.hmset.call_args[0]

        expected_params = {
            u'task_id': self.fake_task.id,
            u'task_name': u'fake_task',
            u'task_status': 'SUCCESS',
            u'user': 'admin', u'arguments': self.fake_task.arguments,
            u'updated_at': 1501177162,
            u'is_new': 1
        }

        self.assertEqual(args[0], 'task_users:admin:123')
        self.assertDictEqual(args[1], expected_params)