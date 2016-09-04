from django import forms
from django.forms import ModelForm
from app.models import Task, Assignment


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ['person', 'task', 'complete']
