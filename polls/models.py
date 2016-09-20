from django.db import models
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey


class Survey(models.Model):

    class Meta:
        verbose_name_plural = 'Surveys'
        ordering = ['the_order']

    title = models.CharField(max_length=100)
    language = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField()
    the_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        if self.active is True:
            active = 'active'
        else:
            active = 'non active'
        time = str(self.created)[:16]
        return self.title + ' -- ' + 'created: ' + time + ' -- ' + active


class Poll(SortableMixin):

    class Meta:
        verbose_name_plural = 'Polls'
        ordering = ['poll_order']

    poll_type = models.CharField(
        max_length=30,
        default='multi',
        choices=(
            ('multi', 'pick multiple options'),
            ('one', 'pick one option'),
            ('countries', 'pick a country from the list'),
            ('text', 'type text'),
            ('email_now', 'email - save and send at Submit'),
            ('email', 'email - just save'),
            ('first_name', 'enter first name'),
        )
    )
    question = models.CharField(max_length=500, blank=True)
    survey = SortableForeignKey(Survey, blank=True)
    first_level = models.BooleanField(default=True)
    poll_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.question


class CharChoice(SortableMixin):

    class Meta:
        verbose_name_plural = 'Choices'
        ordering = ['choice_order']

    choice_text = models.CharField(max_length=200)
    poll = SortableForeignKey(Poll)
    nested = models.ManyToManyField(Poll, blank=True, related_name='nesting_choices')
    choice_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    created_by_visitor = models.BooleanField(default=True)

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


class Email(models.Model):
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    text = models.TextField()
