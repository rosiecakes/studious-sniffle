from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return '{0}'.format(self.title)

    def is_pending(self):
        return bool(self.complete)


class Person(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    shortname = models.CharField(max_length=200, unique=True)
    startdate = models.DateField(auto_now_add=False)
    addeddate = models.DateTimeField(auto_now_add=True)
    tasks = models.ManyToManyField(Task)

    # personalemail = models.EmailField(max_length=50)
    # capability = models.CharField(max_length=50)
    # manager = models.CharField(max_length=50)


    class Meta:
        ordering = ['-addeddate']
        verbose_name_plural = 'people'
        unique_together = ("firstname", "lastname")

    def __str__(self):
        return '{0} {1}'.format(self.firstname, self.lastname)
