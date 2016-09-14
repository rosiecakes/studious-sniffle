from django.contrib import admin, messages

from app.models import Person, Task, Assignment


def assign_all(modeladmin, request, queryset):
    for person in queryset:
        tasks = Task.objects.all()
        count = 0
        for task in tasks:
            obj, created = Assignment.objects.get_or_create(person=person, task=task)
            if created:
                count += 1

    messages.success(request, '{} tasks assigned successfully.'.format(count))

def mark_complete(modeladmin, request, queryset):
    queryset.update(complete=True)

def mark_incomplete(modeladmin, request, queryset):
    queryset.update(complete=False)


assign_all.short_description = "Assign all tasks"
mark_complete.short_description = "Mark selected tasks complete"
mark_incomplete.short_description = "Mark selected tasks incomplete"


class PersonAdmin(admin.ModelAdmin):
    actions = [assign_all]
    readonly_fields = ('addeddate',)

    fieldsets = (
        ('General Information', {
            'fields': ('employtype', 'firstname', 'lastname', 'shortname', 'startdate', 'worksite'),
            'description': "Bold fields are required, but more information is best."
        }),
        ('Contact Information', {
            'fields': ('personalcity', 'personalstate', 'personalemail', 'personalphone', 'workphone'),
            'description': "Home addresses are important for new remote hires, though not necessary for people working at a delivery center and can be left blank."
        }),
        ('Pod Information', {
            'fields': ('capability', 'team', 'kite', 'remote', ),
            'description': "Note for KITE project: the KITE option must be checked to ensure proper task assignment."
        }),
        ('Other Information', {
            'fields': ('csctransfer', 'tokenserial', 'employid', 'cscid'),
            'description': ""
        }))


class AssignmentAdmin(admin.ModelAdmin):
    model = Assignment
    list_display = ['task', 'person', 'comment', 'complete']
    actions = [mark_complete, mark_incomplete]
    list_filter = ['person', 'complete']

    def person(self, obj):
        return obj.person

    def task(self, obj):
        return obj.task


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ['id', 'title', 'stage', 'predecessor_count', 'capability', 'division', 'vpnrequired']
    list_editable = ['title', 'stage', 'capability', 'division', 'vpnrequired']
    list_display_links = ['id']

    def predecessor_count(self, obj):
        return obj.predecessor.count()


admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Task, TaskAdmin)
