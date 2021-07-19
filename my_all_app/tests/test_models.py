from django.test import TestCase
from my_all_app.models import Indicator, Index, Position


class TestIndicator(TestCase):

    def setUp(self):
        self.indicatorDemo = Indicator(name='Test', description="Lorem ipsum dolor"
                                                                " sit amet, consectetur adipiscing elit")

    def test_indicator_name(self):
        self.assertEqual(self.indicatorDemo.retrurnName(), 'Test')

    def test_indicator_description(self):
        self.assertEqual(self.indicatorDemo.retrurnDescription(), "Lorem ipsum dolor"
                                                                  " sit amet, consectetur adipiscing elit")


class TestIndex(TestCase):

    def setUp(self):
        self.indexDemo = Index(name='Test')

    def test_indicator_name(self):
        self.assertEqual(self.indexDemo.retrurnName(), 'Test')

 