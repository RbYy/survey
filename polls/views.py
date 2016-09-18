from django.shortcuts import render
# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from polls.models import *
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    survey = Survey.objects.get(active=True)
    if request.method == 'POST':
        new_visitor = Visitor.objects.create(survey=survey)
        print([f.name for f in Poll._meta.get_fields()])
        allpollfields = [
            (f, f.model if f.model != Poll else None)
            for f in Poll._meta.get_fields()
            if (f.one_to_many or f.one_to_one) and
            f.auto_created and not f.concrete
        ]
        print(allpollfields)
        print('request.POST: ', request.POST)
        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                print(key, ' : ', request.POST[key])

                try:
                    charchoices = CharChoice.objects.filter(pk__in=request.POST.getlist(key))
                    new_visitor.choices.add(*charchoices)
                except:
                    poll = Poll.objects.get(pk=key)
                    text, create = CharChoice.objects.get_or_create(choice_text=request.POST[key], poll=poll)
                    new_visitor.choices.add(text)
                    if poll.poll_type == 'email_now':
                        email = text.choice_text
                        print('email ', email)
                    if poll.poll_type == 'first_name':
                        name = text.choice_text
        try:
            send_mail('Thanks for visiting us',
                      'Hello ' + name +
                      ',\n\nwe hope you enjoyed. Please, come back soon.\nBye,\n\nMuseum',
                      settings.EMAIL_HOST_USER,
                      [email],
                      fail_silently=False)
        except:
            print('email address not valid')

        return HttpResponseRedirect("thankyou/")

    polls = Poll.objects.filter(survey=survey, first_level=True)
    context = {'survey': survey,
               'polls': polls}
    return render(request, 'polls/index.html', context)


def thankyou(request):
    return render(request, 'polls/thankyou.html')


def raport(request):
    visitors = Visitor.objects.all()
    sum_dict = {}
    active_survey = Survey.objects.get(active=True)
    polls = active_survey.poll_set.all()
    for poll in polls:
        sum_dict[poll] = {}
        for choice in poll.charchoice_set.all():
            counter = 0
            for visitor in visitors:
                if choice in visitor.choices.all():
                    counter += 1
            sum_dict[poll][choice.choice_text] = counter

    context = {"polls": polls,
               "sum_dict": sum_dict}
    return render(request, 'polls/raport.html', context)


def details(request):
    visitors = Visitor.objects.all()
    return render(request, 'polls/visitors.html', {'visitors': visitors})
