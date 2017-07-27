# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
class MyDataset(models.Model):
    id = models.AutoField(primary_key=True)
    server_id = models.IntegerField(default=0)
    application_id = models.IntegerField(default=0)
    start_timestamp = models.IntegerField(default=0)

    def __str__(self):
        """This is a MyDataset Model object"""
        return "{}".format(self.name)
