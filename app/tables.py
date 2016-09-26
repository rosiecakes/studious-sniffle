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
