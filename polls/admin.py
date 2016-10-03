from django.contrib import admin
from adminsortable.admin import\
    NonSortableParentAdmin, SortableStackedInline, SortableTabularInline
from polls.models import Survey, Poll, CharChoice, SurveyAttribute, Email, Group
from django.utils.html import format_html


class EmailAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'body',)


class ChoiceSortableTabularInline(SortableStackedInline):
    model = CharChoice
    exclude = ['created_by_visitor']
    extra = 0

    def get_queryset(self, request):
        qs = super(ChoiceSortableTabularInline, self).get_queryset(request)
        return qs.filter(created_by_visitor=False)


class PollTabularInline(SortableTabularInline):
    model = Poll
    fields = ('poll_type', 'question', 'groups', 'first_level', 'include_in_raport',
              'include_in_details', 'ghost')
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
    extra = 0


class SurveyAdmin(NonSortableParentAdmin):
    model = Survey
    fields = ('title', 'description', 'created', 'url',
              ('welcome_letter', 'newsletter', 'hide_ghost'),)
    readonly_fields = ('created', 'url')

    def link(self, obj):
        return format_html(obj.link_to_rendered())

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


class SurveyAttributeAdmin(NonSortableParentAdmin):
    model = SurveyAttribute

    def tab(self, obj):
        return format_html(obj.dicti.dict_table())

    list_display = ('name', 'tab',)


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Group)
admin.site.register(Email, EmailAdmin)
admin.site.register(SurveyAttribute, SurveyAttributeAdmin)
