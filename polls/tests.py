from django.test import TestCase
from polls.models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# Create your tests here.


class SurveyRenderTests(TestCase):
    # fixtures = ['polls_views_testdata.json']

    def test_if_survey_renders(self):
        user = User(username='xxx', email='fdsf@sdf.ss')
        user.save()
        s1 = Survey(user=user, title='hfhff', description='dsfdsf', language='en')
        s1.save()
        print(Survey.objects.all(), s1)
        response = self.client.get(reverse('build_survey', args=(1,)))
        print(response.context)
        print(response.content)
        self.assertEqual(response.status_code, 200)
