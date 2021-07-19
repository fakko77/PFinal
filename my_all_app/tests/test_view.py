from django.test import TestCase, Client
from django.contrib.auth.models import AnonymousUser, User


class ViewsTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            username='fakkotest', password='Morgan771970@')

    def test_index_anonymous_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_all_app/login.html')

    def test_index_login_view(self):
        self.c.force_login(self.user)
        response = self.c.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_all_app/index.html')

    def test_manage_view(self):
        self.c.force_login(self.user)
        response = self.c.get('/my_all/manage/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_all_app/manage.html')

    def test_history_view(self):
        self.c.force_login(self.user)
        response = self.c.get('/my_all/history/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_all_app/history.html')

    def test_calculator_view(self):
        self.c.force_login(self.user)
        response = self.c.get('/my_all/calculator/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_all_app/calculator.html')

    def test_calculator_view(self):
        self.c.force_login(self.user)
        response = self.c.get('/my_all/calculator/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_all_app/calculator.html')

    def test_setting_view(self):
        self.c.force_login(self.user)
        response = self.c.get('/my_all/setting/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_all_app/setting.html')

    def test_add_view(self):
        self.c.force_login(self.user)
        response = self.c.get('/my_all/add/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_all_app/add.html')
