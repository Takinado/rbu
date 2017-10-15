from django.db import models


class Cement(models.Model):
    date = models.DateField(verbose_name='дата', unique=True)
    value = models.IntegerField(verbose_name='количество цемента', default=0)
