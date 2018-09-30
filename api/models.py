from django.db import models
from django.contrib.postgres.fields import JSONField

# Models for Postgres
class Companys(models.Model):
    company = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    data = JSONField()

    #redefining print statement for this object
    def __str__(self):
        new_str = ', '.join([self.company, self.state])
        return new_str

    class Meta:
        """
            can't create primary key because default is id created by Django ORM,
            so create a unique field combining company and state instead
        """
        unique_together = (("company", "state"),)
        """
            verbose_name_plural is for the django admin display, displays Companys
            instead of Companyss
        """
        verbose_name_plural = "Companys"
