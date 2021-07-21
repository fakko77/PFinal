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

"""
class TestPosition(TestCase):

    def setUp(self):
        self.indexDemo1 = Index(name='Test')
        self.indicatorDemo1 = Indicator(id=1, name='Test', description="Lorem ipsum dolor"
                                                                       " sit amet, consectetur adipiscing elit")
        self.positionDemo1 = Position(id=1, position_index=self.indexDemo1, volume="0.05", price="0.1805", be="25",
                                     tp1="50", tp2="75", comment="text", user=1)
        self.positionDemo1.position_indicator.add(self.indicatorDemo1.id)

    def test_position_name_index(self):
        self.assertEqual(self.positionDemo1.position_index.name, self.indexDemo1.name)

    def test_position_indicator(self):
        self.assertEqual(self.positionDemo1.position_indicator.name, self.indicatorDemo1.name)

  
    def test_index_name_indicator(self):
        self.indexDemo1 = Index(name='Test')
        self.indicatorDemo1 = Indicator(id=1, name='Test', description="Lorem ipsum dolor"
                                                                " sit amet, consectetur adipiscing elit")
        self.positionDemo = Position(id=1, position_index=self.indexDemo1, volume="0.05", price="0.1805", be="25",
                                     tp1="50", tp2="75", comment="text", user=1)
        self.positionDemo.position_indicator.add(self.indicatorDemo1.id)
        self.assertEqual(self.positionDemo.position_indicator.name, self.position_indicator.name)

"""



