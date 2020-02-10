from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=1000,
                            blank=False,
                            null=False)

    description = models.CharField(max_length=1000,
                            blank=False,
                            null=False)

    status = models.CharField(max_length=1000, default="OPEN")

    def __str__(self):
        return(self.title)