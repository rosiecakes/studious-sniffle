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

def assign_one(modeladmin, request, queryset):
    for person in queryset:
        task = Task.objects.get(id=46)
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

def mark_complete(modeladmin, request, queryset):
    queryset.update(complete=True)

def mark_incomplete(modeladmin, request, queryset):
    queryset.update(complete=False)


assign_all.short_description = "Assign all tasks"
mark_complete.short_description = "Mark selected tasks complete"
mark_incomplete.short_description = "Mark selected tasks incomplete"
assign_unix_tasks.short_description = "Add UNIX tasks"
assign_wintel_tasks.short_description = "Add Wintel tasks"


class PersonAdmin(admin.ModelAdmin):
    actions = [assign_all, assign_unix_tasks, assign_wintel_tasks, assign_one]
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
    actions = [mark_complete, mark_incomplete]
    list_filter = ['person', 'complete']

    def capability(self, obj):
        return obj.person.capability


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
