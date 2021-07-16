from django.test import TestCase, Client
from django.contrib.auth.models import AnonymousUser, User


class ViewsTest(TestCase):

    def test_index_anonymous(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_all_app/login.html')

    def test_index_login(self):
        c = Client()
        self.user = User.objects.create_user(
            username='fakkotest', password='Morgan771970@')
        c.force_login(self.user)
        response = c.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_all_app/index.html')
