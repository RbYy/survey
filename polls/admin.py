from django.contrib import admin
from adminsortable.admin import\
    NonSortableParentAdmin, SortableStackedInline, SortableTabularInline
from polls.models import Survey, Poll, CharChoice, SurveyAttribute, Email, Group, Visitor, ChoiceGroup
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
    fields = ('poll_type', 'question', 'group', 'first_level', 'include_in_raport',
              'include_in_details', 'ghost')
    extra = 0

    def get_queryset(self, request):
        qs = super(PollTabularInline, self).get_queryset(request)
        survey = qs[0].survey
        if survey.hide_ghost:
            qs = qs.filter(ghost=False)
        return qs


class VisitorAdmin(admin.ModelAdmin):
    def tab(self, obj):
        return format_html(obj.print_visitor())

    model = Visitor
    # list_display = ('tab',)


class SurveyAttributeTabularInline(SortableTabularInline):
    model = SurveyAttribute
    fields = ['name', 'dicti', 'attr_type', 'polls']
    readonly_fields = ['dicti']
    extra = 0


class SurveyAdmin(NonSortableParentAdmin):
    model = Survey
    fields = ('title', 'description', 'created', 'url',
              ('welcome_letter', 'newsletter', 'hide_ghost'), 'update_fixtures')
    readonly_fields = ('created', 'url', 'update_fixtures')

    def update_fixtures(self, obj):
        return format_html('<a href="/build/">Build!</a>')

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
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(SurveyAttribute, SurveyAttributeAdmin)
