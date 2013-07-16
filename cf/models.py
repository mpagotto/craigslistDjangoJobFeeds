from django.db import models

class FeedEntry(models.Model):
    url = models.CharField(max_length=200)
    read_date = models.DateTimeField('date read')
    status = models.CharField(max_length=1)

    def __unicode__(self):
        return self.url