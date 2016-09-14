import django_tables2 as tables
from django_tables2.utils import A

from app.models import Person


class PersonTable(tables.Table):
    shortname = tables.LinkColumn('profile', args=[A('shortname')])

    class Meta:
        model = Person
        attrs = {'class': 'highlight'}
        fields = ('startdate', 'shortname', 'firstname', 'lastname', 'worksite', 'capability', 'employtype',)
