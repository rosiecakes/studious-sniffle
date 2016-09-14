from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


CAPABILITY_CHOICES = (
    ('ADS', 'ADS'),
    ('CDS', 'CDS'),
    ('VDS', 'VDS'),
    ('PCC', 'PCC'),
    ('Active Directory', 'Active Directory'),
    ('Backup', 'Backup'),
    ('Storage', 'Storage'),
    ('Tech Writer', 'Tech Writer'),
    ('UNIX', 'UNIX'),
    ('Wintel', 'Wintel / VM'))

class Task(models.Model):
    BU_CHOICES = (
        ('CSC', 'CSC'),
        ('All UTC', 'All UTC'),
        ('CORP', 'Corp'),
        ('CCS', 'CCS (Carrier/FS)'),
        ('OTIS', 'Otis'),
        ('PW', 'P&W'),
        ('SIK', 'Sik'),
        ('UTAS', 'UTAS'),
        ('UTRC', 'UTRC'))

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=600, blank=True)
    stage = models.CharField(max_length=2, blank=True)
    predecessor = models.ManyToManyField("self", symmetrical=False, blank=True)
    vpnrequired = models.BooleanField(default=False, verbose_name='VPN required for this')
    capability = models.CharField(max_length=20, choices=CAPABILITY_CHOICES, blank=True)
    division = models.CharField(max_length=20, choices=BU_CHOICES, blank=True)

    class Meta:
        ordering = ['title', 'stage', 'id']

    def __str__(self):
        return '{0}'.format(self.title)


class Person(models.Model):
    TEAM_CHOICES = (
        ('iACTION', 'iACTION'),
        ('iBUILD', 'iBUILD'),
        ('iENHANCE', 'iENHANCE'),
        ('iSOLVE', 'iSOLVE'))
    EMPLOY_CHOICES = (
        ('Contractor', 'Contractor'),
        ('Employee', 'Employee'))
    SITE_CHOICES = (
        ('Hartford', 'Hartford'),
        ('Puerto Rico', 'Puerto Rico'))

    firstname = models.CharField(max_length=200, verbose_name='First name')
    lastname = models.CharField(max_length=200, verbose_name='Last name')
    shortname = models.CharField(max_length=200, unique=True, verbose_name='Shortname')
    startdate = models.DateField(auto_now_add=False, verbose_name='Start date')
    addeddate = models.DateTimeField(auto_now_add=True, verbose_name='Date added to status app')

    personalstreet = models.CharField(max_length=50, blank=True, verbose_name='Home street address')
    personalcity = models.CharField(max_length=50, blank=True, verbose_name='Home city')
    personalstate = models.CharField(max_length=50, blank=True, verbose_name='Home state (abbreviation)')
    personalzip = models.CharField(max_length=5, blank=True, verbose_name='Home zip code')
    personalemail = models.EmailField(max_length=50, blank=True, verbose_name='Personal email address')
    personalphone = PhoneNumberField(blank=True, verbose_name='Personal phone number, format: +1 860 888 6060')

    workphone = PhoneNumberField(blank=True, verbose_name='Work phone number')
    workstreet = models.CharField(max_length=50, blank=True, verbose_name='Work street address')
    workcity = models.CharField(max_length=50, verbose_name='Work city', default='Hartford')
    workstate = models.CharField(max_length=50, verbose_name='Work state', default='CT')
    workzip = models.CharField(max_length=5, blank=True, verbose_name='Work zip code')
    worksite = models.CharField(max_length=20, blank=True, choices=SITE_CHOICES, verbose_name="Work site")

    capability = models.CharField(max_length=20, choices=CAPABILITY_CHOICES, default='Wintel', verbose_name='Capability')
    team = models.CharField(max_length=20, choices=TEAM_CHOICES, default='iBUILD')
    kite = models.BooleanField(default=False, verbose_name='Assigned to KITE project')
    remote = models.BooleanField(default=False, verbose_name='Working remotely')
    employid = models.CharField(max_length=15, blank=True, verbose_name='Employee number or PRN')
    employtype = models.CharField(max_length=50, choices=EMPLOY_CHOICES, default='Contractor', verbose_name='Employment Type')
    cscid = models.CharField(max_length=10, blank=True, verbose_name='CSC UTC account name, e.g. XMDS123')

    csctransfer = models.BooleanField(default=False, verbose_name='Existing CSC transfer from another account')
    tokenserial = models.CharField(max_length=15, blank=True, verbose_name='CSC token serial number (if transfer)')

    class Meta:
        ordering = ['-addeddate']
        verbose_name_plural = 'people'
        unique_together = ("firstname", "lastname")

    def __str__(self):
        return '{0} {1}'.format(self.firstname, self.lastname)

    def assignment_count(self):
        return Assignment.objects.filter(person=self, complete=False).count()


class Assignment(models.Model):
    person = models.ForeignKey(Person)
    task = models.ForeignKey(Task)
    comment = models.CharField(max_length=200, blank=True)
    complete = models.BooleanField(default=False)

    class Meta:
        ordering = ['task']

    def __str__(self):
        return self.task.title
