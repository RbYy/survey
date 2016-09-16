from django.shortcuts import render
# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from polls.models import *


def index(request):
    survey = Survey.objects.get(active=True)
    if request.method == 'POST':
        new_visitor = Visitor.objects.create(survey=survey)
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

        return HttpResponseRedirect("thankyou/")

    polls = Poll.objects.filter(survey=survey)
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
