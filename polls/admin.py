from django.contrib import admin
from adminsortable.admin import\
    NonSortableParentAdmin, SortableStackedInline, SortableTabularInline
from polls.models import Survey, Poll, CharChoice, SurveyAttribute, Email, Group, Visitor, ChoiceGroup
from django.utils.html import format_html
from django.conf.urls import *
from django.shortcuts import render


class EmailAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'body',)


class ChoiceSortableTabularInline(SortableStackedInline):
    model = CharChoice
    exclude = ['created_by_visitor']
    filter_horizontal = ('nested',)
    extra = 0

    def get_queryset(self, request):
        qs = super(ChoiceSortableTabularInline, self).get_queryset(request)
        return qs.filter(created_by_visitor=False)


class PollTabularInline(SortableTabularInline):
    model = Poll
    show_change_link = True
    fields = ('poll_type', 'question', 'group', 'first_level', 'include_in_raport',
              'include_in_details', 'ghost',)
    extra = 0

    def get_queryset(self, request):
        qs = super(PollTabularInline, self).get_queryset(request)
        survey = qs[0].survey
        if survey.hide_ghost:
            qs = qs.filter(ghost=False)
        return qs


class SurveyAttributeTabularInline(SortableTabularInline):
    model = SurveyAttribute
    fields = ['name', 'dicti', 'attr_type', 'polls']
    readonly_fields = ['dicti']
    filter_horizontal = ('polls',)
    extra = 0


class SurveyAdmin(NonSortableParentAdmin):
    review_template = 'admin/polls/survey/report.html'
    model = Survey
    fields = ('title', 'description', 'created', 'url',
              ('welcome_letter', 'newsletter', 'hide_ghost'), 'update_fixtures')
    readonly_fields = ('created', 'url', 'update_fixtures')

    def update_fixtures(self, obj):
        return format_html('<a href="/build/">Build!</a>')

    def get_urls(self):
        urls = super(SurveyAdmin, self).get_urls()
        print(urls)
        my_urls = [url(r'report/$', self.report), ]
        return my_urls + urls

    def report(self, request, *args, **kwargs):
        visitors = Visitor.objects.all()
        sum_dict = {}
        # active_survey = Survey.objects.get(active=True)

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

        for survey_attr in SurveyAttribute.objects.filter(include_in_raport=True):
            sum_dict[survey_attr.name] = {}

            for keyval in survey_attr.dicti.keyval_set.all():
                sum_dict[survey_attr.name][keyval.key] = keyval.value

        context = {
            "sum_dict": sum_dict,
            "title": "Report",
            "opts": self.model._meta,
            # "root_path": self.admin_site.root_path
        }
        return render(request, self.review_template, context)

    inlines = [SurveyAttributeTabularInline, PollTabularInline]

    class Media:
        extend = False
        js = ["/static/jquery-3.1.1.js",
              "/static/jquery-ui.min.js",
              "/static/admin/js/custom_inlines.js"
              ]


class PollAdmin(NonSortableParentAdmin):
    model = Poll
    inlines = [ChoiceSortableTabularInline]
    list_display = ('group', 'question', 'poll_type')


class SurveyAttributeAdmin(NonSortableParentAdmin):
    model = SurveyAttribute

    def tab(self, obj):
        try:
            return format_html(obj.dicti.dict_table())
        except:
            return 'still empty'

    list_display = ('name', 'tab',)


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Group)
admin.site.register(ChoiceGroup)
admin.site.register(Email, EmailAdmin)
admin.site.register(Visitor)
admin.site.register(SurveyAttribute, SurveyAttributeAdmin)
admin.site.index_template = 'admin/index.html'
