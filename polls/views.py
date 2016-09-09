from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect


from polls.models import Survey, Poll, CharChoice, Visitor

# Create your views here.


def index(request):
    survey = Survey.objects.get(active=True)
    if request.method == 'POST':
        new_visitor = Visitor.objects.create(survey=survey)
        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                choice = CharChoice.objects.get(pk=request.POST[key])
                new_visitor.choices.add(choice)
                print("resitev!", new_visitor.choices.all())

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
    polls = Survey.objects.get(active=True).poll_set.all()
    for poll in polls:
        sum_dict[poll] = {}
        for choice in poll.charchoice_set.all():
            counter = 0
            for visitor in visitors:
                if choice in visitor.choices.filter():
                    counter += 1
            sum_dict[poll][choice.choice_text] = counter
    context = {"polls": polls,
               "sum_dict": sum_dict}
    return render(request, 'polls/raport.html', context)


def details(request):
    visitors = Visitor.objects.all()
    return render(request, 'polls/visitors.html', {'visitors': visitors})
