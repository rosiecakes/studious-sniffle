from django.contrib import admin

from app.models import Person, Task, Assignment


admin.site.register(Task)


# class AssignmentInline(admin.StackedInline):
#     model = Assignment

class PersonAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General Information', {
            'fields': ('firstname', 'lastname', 'shortname', 'startdate', 'workemail', 'employtype')
        }),
        ('Tasks:', {
            'classes': ('collapse',),
            'fields': ('lastname',),
        }),
    )

    # inlines = [AssignmentInline]


admin.site.register(Person, PersonAdmin)


def mark_complete(modeladmin, request, queryset):
    queryset.update(complete=True)

def mark_incomplete(modeladmin, request, queryset):
    queryset.update(complete=False)

mark_complete.short_description = "Mark selected tasks complete"
mark_incomplete.short_description = "Mark selected tasks incomplete"

class AssignmentAdmin(admin.ModelAdmin):
    model = Assignment
    list_display = ['task', 'person', 'complete']
    actions = [mark_complete, mark_incomplete]

    def person(self, obj):
        return obj.person

    def task(self, obj):
        return obj.task


admin.site.register(Assignment, AssignmentAdmin)
