from django import forms
from app.models import Task


class TaskForm(forms.Form):
    complete = forms.BooleanField(required=False)
    tasks = Task.objects.all()

    class Meta:
        model = Task
