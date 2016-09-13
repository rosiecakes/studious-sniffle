import django_tables2 as tables
from app.models import Person


class PersonTable(tables.Table):
    class Meta:
        model = Person
        cscid_table = tables.Column(accessor='cscid')
        
        fields = ('startdate', 'shortname', 'firstname', 'lastname', 'worksite', 'capability', 'kite', 'employtype', 'cscid_table')
