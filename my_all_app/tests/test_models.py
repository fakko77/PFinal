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
        self.indicatorDemo = Indicator(name='Test', description="Lorem ipsum dolor"
                                                                " sit amet, consectetur adipiscing elit")

    def test_indicator_name(self):
        self.assertEqual(self.indexDemo.retrurnName(), 'Test')


class TestPosition(TestCase):

    def setUp(self):
        self.indexDemo = Index(name='Test')
        self.indexDemo.save()
        self.indicatorDemo = Indicator(name='Test', description="Lorem ipsum dolor"
                                                                " sit amet, consectetur adipiscing elit")
        self.indicatorDemo.save()
        self.positionDemo = Position(position_index=self.indexDemo, volume="0.05", price="0.1805", be="25",
                                     tp1="50", tp2="75", comment="text")
        self.positionDemo.save()
        self.positionDemo.position_indicator.add(self.indicatorDemo.id)
        self.positionDemo.save()

    def test_position_name_index(self):
        self.assertEqual(self.positionDemo.position_index.name, self.indexDemo.name)

    def test_position_indicator_notequal(self):
        self.assertNotEqual(self.positionDemo.position_indicator, self.indicatorDemo.name)






