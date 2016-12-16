from django.test import TestCase
from polls.models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.files import File
# Create your tests here.


class SurveyRenderTests(TestCase):
    # fixtures = ['polls_views_testdata.json']

    def test_if_survey_renders(self):
        user = User(username='xxx', email='fdsf@sdf.ss')
        user.save()
        s1 = Survey(user=user, title='SurveyTitle', description='dsfdsf', language='en')
        s1.save()
        response = self.client.get(reverse('build_survey', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<p class="headline">SurveyTitle</p>')

    def test_if_logo_loads(self):
        user = User(username='xxx', email='fdsf@sdf.ss')
        user.save()
        f = open('053.JPG', 'rb')
        s1 = Survey(user=user, title='SurveyTitle', description='dsfdsf', language='en', logo=File(f))
        s1.save()
        response = self.client.get(reverse('build_survey', args=(1,)))
        print(response.content)
        self.assertContains(response, '053.JPG')
