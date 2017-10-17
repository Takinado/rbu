from django.db import models


class CementManager(models.Manager):
    def create_cement(self, date, value):
        cement = self.create(date=date, value=value)
        # do something with the cement
        return cement


class Cement(models.Model):
    date = models.DateField(verbose_name='дата', unique=True)
    value = models.IntegerField(verbose_name='количество цемента', default=0)

    objects = CementManager()

    def __str__(self):
        return '{}'.format(self.date.strftime("%d.%m.%Y"))

    class Meta:
        ordering = ['-date', ]
        verbose_name = 'Отчет по цементу'
        verbose_name_plural = 'Отчеты по цементу'
