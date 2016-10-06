from django.shortcuts import render
# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from polls.models import *
from django.core.mail import send_mail
from django.conf import settings


def build_survey(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    name = ''
    if request.method == 'POST':
        new_visitor = Visitor.objects.create(survey=survey)
        data = Dicty.objects.create(name=new_visitor.pk)
        print('request.POST: ', request.POST)
        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                poll = Poll.objects.get(pk=key)

                if poll.poll_type == 'multi':
                    charchoices = CharChoice.objects.filter(
                        pk__in=request.POST.getlist(key))
                    new_visitor.choices.add(*charchoices)
                    KeyVal.objects.create(
                        container=data,
                        key=poll.group.name,
                        value=str([choice.group.name for choice in charchoices]))
                    new_visitor.collected_data = data
                    new_visitor.save()

                elif poll.poll_type == 'one':
                    choice = CharChoice.objects.get(
                        pk=request.POST[key])
                    new_visitor.choices.add(choice)
                    KeyVal.objects.create(
                        container=data,
                        key=poll.group.name,
                        value=choice.group.name)
                    new_visitor.collected_data = data
                    new_visitor.save()

                else:
                    choice, create = CharChoice.objects.get_or_create(
                        choice_text=request.POST[key],
                        poll=poll,
                        created_by_visitor=True)
                    new_visitor.choices.add(choice)
                    KeyVal.objects.create(
                        container=data,
                        key=poll.group.name,
                        value=choice)
                    new_visitor.collected_data = data
                    new_visitor.save()

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
            split_body = survey.welcome_letter.body.split('//')
            body = ''
            for part in split_body:
                if part == 'first_name':
                    part = name
                body += part
            send_mail(
                'Thanks for visiting us',
                body,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False)

        except:
            print('email address not valid')

        return HttpResponseRedirect("/thankyou/")

    polls = Poll.objects.filter(survey=survey, first_level=True)
    context = {'survey': survey,
               'polls': polls}
    return render(request, 'polls/index.html', context)


def thankyou(request):
    return render(request, 'polls/thankyou.html')


def send_newsletter_view(request):
    pass


def build_fixture(request):
    for choice in CharChoice.objects.filter(created_by_visitor=False):
        if not choice.group:
            choice.group = ChoiceGroup.objects.create(name=choice.choice_text)
    for poll in Poll.objects.all():
        if not poll.group:
            poll.group = Group.objects.create(name=poll.question)
    return HttpResponseRedirect("/thankyou/")


def report(request):
    visitors = Visitor.objects.all()
    sum_dict = {}
    active_survey = Survey.objects.get(active=True)

    included_poll_groups = [poll.group.name for poll in Poll.objects.filter(include_in_raport=True)]
    for visitor in visitors:
        for keyval in visitor.collected_data.keyval_set.all():
            if keyval.key in included_poll_groups:
                if keyval.key not in sum_dict.keys():
                    sum_dict[keyval.key] = {}
                for choice in keyval.listify():
                    if choice not in sum_dict[keyval.key].keys():
                        sum_dict[keyval.key][choice] = 0
                    sum_dict[keyval.key][choice] += 1

    for survey_attr in active_survey.surveyattribute_set.filter(include_in_raport=True):
        sum_dict[survey_attr.name] = {}

        for keyval in survey_attr.dicti.keyval_set.all():
            sum_dict[survey_attr.name][keyval.key] = keyval.value

    context = {"sum_dict": sum_dict}
    return render(request, 'polls/report.html', context)


def details(request):
    visitors = Visitor.objects.all()
    return render(request, 'polls/visitors.html', {'visitors': visitors})
