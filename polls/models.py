from django.db import models
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey
from django.utils.html import format_html


class Email(models.Model):
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.title


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
    hide_ghost = models.BooleanField(default=True)
    welcome_letter = models.ForeignKey(Email, null=True, blank=True, related_name='survey_welcome')
    newsletter = models.ForeignKey(Email, null=True, blank=True, related_name='survey_newsletter')
    publish_url = models.URLField(null=True, blank=True)

    def __str__(self):
        if self.active is True:
            active = 'active'
        else:
            active = 'non active'
        time = str(self.created)[:16]
        return self.title + ' -- ' + 'created: ' + time + ' -- ' + active

    def send_newsletter(self):
        pass


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
    include_in_raport = models.BooleanField(default=True)
    include_in_details = models.BooleanField(default=True)
    ghost = models.BooleanField(default=False)

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
    created_by_visitor = models.BooleanField(default=False)

    def __str__(self):

        return self.choice_text


class Visitor(models.Model):
    filled = models.DateTimeField(auto_now_add=True)
    survey = models.ForeignKey(Survey)
    choices = models.ManyToManyField(CharChoice)
    subscribed = models.BooleanField(default=True)

    def CollectData(self):
        polls = self.survey.poll_set.filter(include_in_details=True)
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


class Dicty(models.Model):
    name = models.CharField(max_length=50)

    def dict_table(self):
        result = '<table><tbody class="dicty-table"><tr><th>' + self.name + '</th><th></th><tr>'
        for pair in self.keyval_set.all():
            line = '<tr><td>' + pair.key + '</td><td>' + pair.value + '</td></tr>' + '\n'
            result += line
        result += '</tbody></table>'
        return format_html(result)

    def __str__(self):
        return self.dict_table()


class KeyVal(models.Model):
    container = models.ForeignKey(Dicty)
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=150, default=0)


class SurveyAttribute(SortableMixin):
    class Meta:
        verbose_name_plural = 'Survey Attributes'
        ordering = ['attr_order']

    name = models.CharField(max_length=30)
    survey = SortableForeignKey(Survey)
    dicti = models.ForeignKey(Dicty, blank=True, null=True, verbose_name='values')
    attr_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    attr_type = models.CharField(
        verbose_name='action',
        max_length=30,
        choices=(
            ('summarize', 'summarize'),
            ('count', 'count answers'),
            ('average', 'calc average'),
        )
    )
    polls = models.ManyToManyField(Poll)
    include_in_raport = models.BooleanField(default=True)

    def summarize(self, choice_input):
        d, c = Dicty.objects.get_or_create(name=self.name)
        kv, cc = KeyVal.objects.get_or_create(container=d, key='Total')
        kv.value = int(kv.value) + int(choice_input)
        kv.save()
        self.dicti = d
        self.save()

    def count(self, poll, choice_input):
        d, c = Dicty.objects.get_or_create(name=self.name)
        ch = CharChoice.objects.get(pk=choice_input.pk)
        kv, cc = KeyVal.objects.get_or_create(container=d, key=ch.choice_text)
        kv.value = int(kv.value) + 1
        kv.save()
        self.dicti = d
        self.save()

    def __str__(self):
        return self.name
