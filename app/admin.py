from django.contrib import admin, messages

from app.models import Person, Task, Assignment
from app.forms import AssignmentForm


def assign_all(modeladmin, request, queryset):
    for person in queryset:
        tasks = Task.objects.all()
        for task in tasks:
            assignment = Assignment(person=person, task=task)
            assignment.save()

    messages.success(request, 'All tasks assigned')


assign_all.short_description = "Assign all tasks"

class PersonAdmin(admin.ModelAdmin):
    actions = [assign_all]
    readonly_fields = ('addeddate',)

    fieldsets = (
        ('General Information', {
            'fields': ('firstname', 'lastname', 'shortname', 'startdate', 'employtype', 'employid')
        }),
        ('Contact Information', {
            'fields': ('personalemail', 'personalphone', 'workphone')
        }),
        ('Pod Information', {
            'fields': ('capability', 'team', 'kite', 'remote', 'csctransfer', 'tokenserial')
        }),
        ('Other', {
            'classes': ('collapse',),
            'fields': ('capability',),
        }),
    )


def mark_complete(modeladmin, request, queryset):
    queryset.update(complete=True)

def mark_incomplete(modeladmin, request, queryset):
    queryset.update(complete=False)

mark_complete.short_description = "Mark selected tasks complete"
mark_incomplete.short_description = "Mark selected tasks incomplete"

class AssignmentAdmin(admin.ModelAdmin):
    model = Assignment
    list_display = ['task', 'person', 'comment', 'complete']
    actions = [mark_complete, mark_incomplete]

    def person(self, obj):
        return obj.person

    def task(self, obj):
        return obj.task


admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Task)
