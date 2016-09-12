from django.shortcuts import render
# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Count
from polls.models import *

# Create your views here.


def index(request):
    survey = Survey.objects.get(active=True)
    if request.method == 'POST':
        new_visitor = Visitor.objects.create(survey=survey)
        for key in request.POST:
            if key.startswith('idpoll'):
                charchoices = CharChoice.objects.filter(pk__in=request.POST.getlist(key))
                new_visitor.choices.add(*charchoices)
            if key.startswith('idtextpoll'):
                question = key[11:]
                textpoll = TextPoll.objects.get(question=question)
                text = TextEnter.objects.create(label=question, text=request.POST[key], poll=textpoll)
                new_visitor.textentries.add(text)
            if key.startswith('country'):
                pk = key[8:]
                poll = Poll.objects.get(pk=pk)
                country, create = CharChoice.objects.get_or_create(choice_text=request.POST[key], poll=poll)
                new_visitor.choices.add(country)

        return HttpResponseRedirect("thankyou/")

    polls = Poll.objects.filter(survey=survey)
    textpolls = TextPoll.objects.filter(survey=survey)
    context = {'survey': survey,
               'polls': polls,
               'textpolls': textpolls}
    return render(request, 'polls/index.html', context)


def thankyou(request):
    return render(request, 'polls/thankyou.html')


def raport(request):
    visitors = Visitor.objects.all()
    sum_dict = {}
    active_survey = Survey.objects.get(active=True)
    polls = active_survey.poll_set.all()
    textpolls = active_survey.textpoll_set.all()
    for poll in polls:
        sum_dict[poll] = {}
        for choice in poll.charchoice_set.all():
            counter = 0
            for visitor in visitors:
                if choice in visitor.choices.all():
                    counter += 1
            sum_dict[poll][choice.choice_text] = counter

    for textpoll in textpolls:
        sum_dict[textpoll] = {}
        distinct = set()

        for enter in TextEnter.objects.filter(poll=textpoll):
            distinct.add(enter.text)
        for text in distinct:
            counter = 0
            for enter in TextEnter.objects.filter(poll=textpoll):
                if text == enter.text:
                    counter += 1
            sum_dict[textpoll][text] = counter
    context = {"polls": polls,
               "sum_dict": sum_dict}
    return render(request, 'polls/raport.html', context)


def details(request):
    visitors = Visitor.objects.all()
    return render(request, 'polls/visitors.html', {'visitors': visitors})
