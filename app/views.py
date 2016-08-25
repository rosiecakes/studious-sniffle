from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.contrib import messages

from app.models import Person, Task
from app.forms import TaskForm


def index(request):
    people = Person.objects.order_by('startdate')
    return render(request, 'app/index.html',
        {'people': people})


@require_http_methods(["GET", "POST"])
def profile(request, shortname):
    people = Person.objects.order_by('startdate')
    person = Person.objects.get(shortname = shortname)
    tasks = Person.objects.get(shortname = shortname).tasks.all()
    form = TaskForm(request.POST or None)

    if request.method == "POST":
        check_values = request.POST.getlist('task')

        for check in check_values:
            task = person.tasks.get(id = check)
            task.complete = True
            task.save()
            message = messages.success(request, 'Task marked complete')

        message = messages.success(request, 'after the check')
        # return HttpResponseRedirect(reverse('views.profile', args=(shortname)))
        # return render(request, 'app/profile.html', {'message': messages})

    elif request.method == "POST":
        return messages.success(request, 'Request was post but task did not get marked')

    context = {'shortname': shortname,
                'people': people,
                'person': person,
                'tasks': tasks,
                'form': form,
                'message': messages}

    return render(request, 'app/profile.html', context)
