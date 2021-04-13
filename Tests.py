from unittest import TestCase
from ThreadingManager import tasks_divider


class Tester(TestCase):
    def setUp(self) -> None:
        pass

    def test_tasks_divider_normal_list(self):
        tasks1 = [1, 2, 3, 4, 5, 6]
        self.assertEqual(tasks_divider(tasks1, 3), [[1, 2, 3], [4, 5, 6]])

    def test_tasks_divider_short_list(self):
        tasks2 = [1]
        self.assertEqual(tasks_divider(tasks2, 5), [[1]])

    def test_tasks_divider_empty_list(self):
        tasks3 = []
        self.assertEqual(tasks_divider(tasks3, 6), [[]])

    def test_tasks_divider_very_long_list(self):
        tasks4 = [1] * 99
        self.assertEqual(len(tasks_divider(tasks4, 17)), 99 // 17 + 1)
