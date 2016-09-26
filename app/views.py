from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

import random
from django_tables2 import RequestConfig

from app.models import Person, Task, Assignment
from app.forms import AssignmentForm
from app.tables import PersonTable


@receiver(post_save, sender=Person)
def my_handler(sender, **kwargs):
    """
    Create new assignments when a new person is added. Get the person, the tasks,
    then add them and their predecessor tasks, to the person as 'assignments'.
    """
    person = Person.objects.latest('addeddate')
    tasks = Task.objects.all().filter(Q(division='All UTC') | Q(division='CSC') | Q(capability=person.capability))

    if person.kite:
        tasks = Task.objects.all().filter(Q(division='CSC') | Q(division='SIK') & Q(capability=person.capability))

    if person.capability == 'Backup':
        tasks = Task.objects.all().filter(Q(division='All UTC') | Q(division='CSC') | Q(capability='UNIX') | Q(capability='Wintel') | Q(capability='Backup'))

    def create_new_tasks(person, task):
        obj, created = Assignment.objects.get_or_create(person=person, task=task)

    for task in tasks:
        create_new_tasks(person=person, task=task)
        for task in task.predecessor.all():
            create_new_tasks(person=person, task=task)


def index(request):
    """Pass the lastest people created to the index view."""
    table = PersonTable(Person.objects.all())
    RequestConfig(request).configure(table)

    people = Person.objects.order_by('firstname')
    return render(request, 'app/index.html',
        {'people': people, 'table':table})


@require_http_methods(["GET", "POST"])
def profile(request, shortname=None):
    """
    Get people and their tasks and pass them to the view. Update tasks (their
    completion) depending on user POST input (which boxes they checked).
    """
    people = Person.objects.order_by('firstname')
    person = get_object_or_404(Person, shortname=shortname)
    assignments = Assignment.objects.filter(person=person)
    randimg = random.randint(1, 20)
    form = AssignmentForm(request.POST or None)

    if request.method == "POST":
        check_values = request.POST.getlist('assignment')

        for check in check_values:
            task = Assignment.objects.get(id=check)
            task.complete = True
            task.save()
            messages.success(request, 'Task(s) marked complete')

    context = {'shortname': shortname,
                'people': people,
                'person': person,
                'assignments': assignments,
                'form': form,
                'message': messages,
                'randimg': randimg}

    return render(request, 'app/profile.html', context)
