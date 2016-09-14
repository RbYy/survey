from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=100)
    language = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField()

    def __str__(self):
        if self.active is True:
            active = 'active'
        else:
            active = 'non active'
        time = str(self.created)[:16]
        return self.title + ' -- ' + 'created: ' + time + ' -- ' + active


class Poll(models.Model):
    poll_type = models.CharField(max_length=30, default='multi',
        choices=(
                ('multi', 'pick multiple options'),
                ('one', 'pick one option'),
                ('countries', 'pick a country from the list'),
                ('text', 'type text'),
        )
    )
    question = models.CharField(max_length=500, blank=True)
    survey = models.ManyToManyField(Survey)

    def __str__(self):
        return self.question


class CharChoice(models.Model):
    choice_text = models.CharField(max_length=200)
    poll = models.ForeignKey(Poll)

    def __str__(self):

        return self.choice_text


class Visitor(models.Model):
    filled = models.DateTimeField(auto_now_add=True)
    survey = models.ForeignKey(Survey)
    choices = models.ManyToManyField(CharChoice)

    def CollectData(self):
        polls = self.survey.poll_set.all()
        return [(poll,
                 [choice.choice_text for choice in
                  self.choices.filter(poll=poll)])for poll in polls]

    def PrintVisitor(self):
        print(self.CollectData())
        time = str(self.filled)[:16]
        data = self.CollectData()
        rendered = ''
        for text in data:
            rendered += ' -- '
            for i in text:
                rendered += str(i) + ' '
        return time + rendered

    def __str__(self):
        return self.PrintVisitor()
