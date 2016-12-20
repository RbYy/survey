from django.test import TestCase
from polls.models import *
#from django.db import IntegrityError
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.files import File


class SurveyRenderTests(TestCase):
    # fixtures = ['polls_views_testdata.json']
    def setUp(self):
        user = User(username='xxx', email='fdsf@sdf.ss')
        user.save()
        self.s1 = Survey(
            user=user,
            title='SurveyTitle',
            description='dsfdsf',
            language='en',
            # logo=File(open('053.JPG', 'rb'))
        )
        self.s1.save()
        self.response = self.client.get(reverse('build_survey', args=(1,)))

    def test_if_survey_renders(self):

        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, '<p class="headline">SurveyTitle</p>')

    def test_if_logo_loads(self):
        # self.assertContains(self.response, '053.JPG')
        pass


class RegistrationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='xxx', email='fdsf@sdf.ss', password='secret')

    def test_logging_in(self):
        response = self.client.post(
            reverse('admin:login'),
            {'next': '/admin/', 'username': 'xxx', 'password': 'secret'},
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome')
        self.assertContains(self.client.get(reverse('admin:index'), follow=True), 'Welcome')
        response = self.client.post(
            reverse('admin:login'),
            {'next': '/admin/', 'username': 'yyy', 'password': 'secret'}, follow=True)
        self.assertContains(response, 'Please enter the correct username and password')

    def test_register(self):
        response = self.client.post(
            reverse('register'),
            {'username': 'xxx', 'email': 'yyy@yyy.yy', 'password1': 'secret', 'password2': 'secret'})
        self.assertContains(response, 'The username already exists.')
        response = self.client.post(
            reverse('register'),
            {'username': 'yyy', 'email': 'yyy@xxx.yy', 'password1': 'secret1', 'password2': 'secret1'}, follow=True)
        self.assertEqual(response.redirect_chain[0], ('/admin/', 302))
        self.assertTrue(User.objects.get(username='yyy'))

