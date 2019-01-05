from django.db import models


class TimeStampedModel(models.Model):
    '''
    An abstract class model that provides self-updating
    "creation_date" and "modification_date" fields.
    '''

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
