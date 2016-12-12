from django.shortcuts import render
# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from polls.models import *
from django.conf import settings
from polls.forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.core.cache import cache
cache.clear()


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(
                username=username,
                password=password,
                email=form.cleaned_data['email'],
                is_staff=True
            )
            for perm in range(16, 500):
                try:
                    user.user_permissions.add(perm)
                except:
                    pass
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/admin/')
    else:
        form = RegistrationForm()

    return render(request, 'admin/registration.html', {'form': form})


def build_survey(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    name = ''
    if request.method == 'POST':
        new_visitor = Visitor.objects.create(survey=survey, user=survey.user)
        data = Dicty.objects.create(name=new_visitor.pk)
        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                poll = Poll.objects.get(pk=key)

                if poll.poll_type == 'multi':
                    poll.multichoice_handle(request, key, new_visitor, data)
                elif poll.poll_type == 'one':
                    poll.onechoice_handle(request, key, new_visitor, data)
                else:
                    choice = poll.textinput_handle(request, key, new_visitor, data, survey)

                for survey_attr in survey.surveyattribute_set.all():
                    if poll in survey_attr.polls.all():
                        if survey_attr.attr_type == 'summarize':
                            survey_attr.summarize(int(choice.choice_text))
                        if survey_attr.attr_type == 'count':
                            survey_attr.count(poll, choice)

                if poll.poll_type == 'email_now':
                    email = choice.choice_text

                if poll.poll_type == 'first_name':
                    name = choice.choice_text
        try:
            survey.send_welcome_letter(email, name)

            if survey.notify:
                survey.send_submit_notification_email(new_visitor)
        except UnboundLocalError:
            print('no email provided')

        return HttpResponseRedirect("/thankyou/")

    polls = Poll.objects.filter(survey=survey, first_level=True)
    context = {'survey': survey,
               'polls': polls}
    return render(request, 'polls/index.html', context)


def thankyou(request):
    return render(request, 'polls/thankyou.html')


def build_fixture(request):
    for choice in CharChoice.objects.filter(created_by_visitor=False):
        if not choice.group:
            choice.group = ChoiceGroup.objects.create(name=choice.choice_text)
    for poll in Poll.objects.all():
        if not poll.group:
            poll.group = PollGroup.objects.create(name=poll.question)
    return HttpResponseRedirect("/thankyou/")
