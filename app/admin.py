from django.contrib import admin, messages

from app.models import Person, Task, Assignment, Domain


def assign_all(modeladmin, request, queryset):
    for person in queryset:
        tasks = Task.objects.all()
        count = 0
        for task in tasks:
            obj, created = Assignment.objects.get_or_create(person=person, task=task)
            if created:
                count += 1

    messages.success(request, '{} tasks assigned successfully.'.format(count))

def assign_unix_tasks(modeladmin, request, queryset):
    for person in queryset:
        tasks = Task.objects.filter(capability='UNIX')
        count = 0
        for task in tasks:
            obj, created = Assignment.objects.get_or_create(person=person, task=task)
            if created:
                count += 1

    messages.success(request, '{} tasks assigned successfully.'.format(count))

def assign_wintel_tasks(modeladmin, request, queryset):
    for person in queryset:
        tasks = Task.objects.filter(capability='Wintel')
        count = 0
        for task in tasks:
            obj, created = Assignment.objects.get_or_create(person=person, task=task)
            if created:
                count += 1

    messages.success(request, '{} tasks assigned successfully.'.format(count))

def set_assignment_color(modeladmin, request, queryset):
    colors = ['deep-orange-text', 'cyan-text', 'deep-purple-text']
    count = 0
    for a in queryset:
        if a.task.stage == "1":
            a.divclass = colors[0]
        if a.task.stage == "2":
            a.divclass = colors[1]
        if a.task.stage == "3":
            a.divclass = colors[2]
        a.save()
        count += 1

    messages.success(request, '{} task colors changed successfully.'.format(count))

def assign_task_to_all_people(modeladmin, request, queryset):
    for task in queryset:
        count = 0
        for person in Person.objects.all():
            obj, create = Assignment.objects.get_or_create(person=person, task=task)
            count += 1

    messages.success(request, '{} new assignments created for {}.'.format(count, task))

def mark_complete(modeladmin, request, queryset):
    queryset.update(complete=True)

def mark_incomplete(modeladmin, request, queryset):
    queryset.update(complete=False)


assign_all.short_description = "Assign all tasks"
mark_complete.short_description = "Mark selected tasks complete"
mark_incomplete.short_description = "Mark selected tasks incomplete"
assign_unix_tasks.short_description = "Add UNIX tasks"
assign_wintel_tasks.short_description = "Add Wintel tasks"
set_assignment_color.short_description = "Set color of task stage"
assign_task_to_all_people.short_description = "Add task as assignment for everyone"


class PersonAdmin(admin.ModelAdmin):
    actions = [assign_all, assign_unix_tasks, assign_wintel_tasks]
    readonly_fields = ['addeddate',]
    list_display = ['name', 'shortname', 'capability', 'team', 'cscid']
    list_filter = ['worksite', 'kite', 'employtype', 'capability', 'team']
    list_display_links = ['name', 'shortname']
    list_editable = ['cscid']

    def name(self, obj):
        return '{} {}'.format(obj.firstname, obj.lastname)

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
            'fields': ('csctransfer', 'tokenserial', 'employid', 'cscid', 'nonadmindomain', 'admindomains'),
            'description': ""
        }))


class AssignmentAdmin(admin.ModelAdmin):
    model = Assignment
    list_display = ['task', 'person', 'capability', 'comment', 'complete']
    actions = [mark_complete, mark_incomplete, set_assignment_color]
    list_filter = ['person', 'complete']
    fieldsets = (
        (None, {
            'fields': ('person', 'task', 'comment', 'whosubmitted', 'processing', 'complete')
        }),)

    def capability(self, obj):
        return obj.person.capability


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ['id', 'title', 'stage', 'predecessor_count', 'capability', 'division', 'vpnrequired']
    list_editable = ['title', 'stage', 'capability', 'division', 'vpnrequired']
    list_display_links = ['id']
    actions = [assign_task_to_all_people]

    def predecessor_count(self, obj):
        return obj.predecessor.count()


admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Task, TaskAdmin)
