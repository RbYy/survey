from django.contrib import admin
from adminsortable.admin import\
    NonSortableParentAdmin, SortableStackedInline, SortableTabularInline
from polls.models import Survey, Poll, CharChoice, SurveyAttribute, Dicty


class ChoiceSortableTabularInline(SortableStackedInline):
    model = CharChoice
    exclude = ['created_by_visitor']
    extra = 0

    def get_queryset(self, request):
        qs = super(ChoiceSortableTabularInline, self).get_queryset(request)
        return qs.filter(created_by_visitor=False)


class PollTabularInline(SortableTabularInline):
    model = Poll
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
    inlines = [SurveyAttributeTabularInline, PollTabularInline]


class PollAdmin(NonSortableParentAdmin):
    model = Poll
    inlines = [ChoiceSortableTabularInline]


class SurveyAttributeAdmin(NonSortableParentAdmin):
    model = SurveyAttribute
    inlines = [PollTabularInline]


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Dicty)
admin.site.register(CharChoice)
# admin.site.register(SurveyAttribute, Admin)
