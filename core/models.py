import datetime
from django.db import models


class TimeStampedModel(models.Model):
    '''
    An abstract class model that provides self-updating
    "creation_date" and "modification_date" fields.
    '''

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.modification_date = datetime.date.today()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    class Meta:
        abstract = True
