from django.test import TestCase, Client
from django.contrib.auth.models import User
from my_all_app.forms import IndexForm, IndicatorForm, PositionForm


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
    def test_form_is_valid(self):
        form_data = {'position_index': 'position_index', 'volume': '0.05', 'be': '25', 'tp1': '10',
                     'tp2': '15', 'position_indicator': 'position_indicator', 'comment': 'comment'}
        form = PositionForm(data=form_data)
        self.assertTrue(form.is_valid())
