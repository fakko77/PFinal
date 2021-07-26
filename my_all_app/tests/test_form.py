from django.test import TestCase, Client
from django.contrib.auth.models import User
from my_all_app.forms import IndexForm, IndicatorForm, PositionForm
from my_all_app.models import Indicator, Index, Position


class TestIndexForm(TestCase):
    def test_form_is_valid(self):
        form_data = {'name': 'name'}
        form = IndexForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_false(self):
        form_data = {'name': ''}
        form = IndexForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestIndicatorForm(TestCase):
    def test_form_is_valid(self):
        form_data = {'name': 'name', 'description': 'description'}
        form = IndicatorForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_false(self):
        form_data = {'name': '', 'description': ''}
        form = IndicatorForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestPositionForm(TestCase):
    def setUp(self):
        index = Index(id=1, name='EURUSD')
        index.save()
        indicator = Indicator(name='EURUSD', description="test")
        indicator.save()
        self.Index = Index.objects.get(id=1)
        self.indicator = Indicator.objects.all()

    def test_form_is_valid(self):
        form_data = {'position_index': self.Index, 'volume': '1',
                     'be': '25', 'sl': '25', 'tp1': '10',
                     'tp2': '15', 'position_indicator': self.indicator,
                     'comment': 'comment'}
        form = PositionForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_form_is_false(self):
        form_data = {'position_index': 'position_index',
                     'volume': '0.05', 'sl': '25', 'be': '25', 'tp1': '10',
                     'tp2': '15', 'position_indicator': 'position_indicator',
                     'comment': 'comment'}
        form = PositionForm(data=form_data)
        self.assertFalse(form.is_valid())
