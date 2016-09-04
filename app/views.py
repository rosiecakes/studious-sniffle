from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

import random

from app.models import Person, Task, Assignment
from app.forms import AssignmentForm


def index(request):
    people = Person.objects.order_by('startdate')
    return render(request, 'app/index.html',
        {'people': people})


@require_http_methods(["GET", "POST"])
def profile(request, shortname=None):
    people = Person.objects.order_by('startdate')
    person = get_object_or_404(Person, shortname=shortname)
    tasks = Assignment.objects.filter(person=person)
    randimg = random.randint(1, 6)
    form = AssignmentForm(request.POST or None)

    if request.method == "POST":
        check_values = request.POST.getlist('task')

        for check in check_values:
            task = Assignment.objects.get(id=check)
            task.complete = True
            task.save()
            messages.success(request, 'Task marked complete')

    context = {'shortname': shortname,
                'people': people,
                'person': person,
                'tasks': tasks,
                'form': form,
                'message': messages,
                'randimg': randimg}

    return render(request, 'app/profile.html', context)
