import django_tables2 as tables
from django_tables2.utils import A

from app.models import Person, Assignment


class PersonTable(tables.Table):
    shortname = tables.LinkColumn('profile', args=[A('shortname')])
    tasks = tables.Column(accessor='assignment_count', orderable=False)

    class Meta:
        model = Person
        attrs = {'class': 'highlight'}
        fields = ('tasks', 'startdate', 'shortname', 'firstname', 'lastname', 'cscid', 'worksite', 'capability', 'employtype')


class AssignmentTable(tables.Table):
    capability = tables.Column(accessor='capability', orderable=False)
    bu_columns = tables.Column(accessor='bu_columns', orderable=False)

    class Meta:
        model = Assignment
        attrs = {'class': 'highlight'}
        fields = ('person', 'processing', 'complete')
