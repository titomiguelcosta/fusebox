from django.test import TestCase


class TestSlack(TestCase):
    def test_true(self):
        assert 1 == 1

    def test_false(self):
        assert 0 == 0
