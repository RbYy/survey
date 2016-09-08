from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=100)
    language = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField()

    def __str__(self):
        return self.title + ' created: ' + self.created + 'active: ' + self.active


class Poll(models.Model):
    question = models.CharField(max_length=500)
    survey = models.ManyToManyField(Survey)

    def __str__(self):
        return self.question


class CharChoice(models.Model):
    choice_text = models.CharField(max_length=200)
    poll = models.ForeignKey(Poll)


class EmailChoice(models.Model):
    choice_text = models.EmailField()
    poll = models.ForeignKey(Poll)

    def __unicode__(self):
        return self.choice_text


class Visitor(models.Model):
    filled = models.DateTimeField(auto_now_add=True)
    survey = models.ForeignKey(Survey)
    choices = models.ManyToManyField(CharChoice)
