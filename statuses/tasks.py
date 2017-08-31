from __future__ import absolute_import, unicode_literals
import random
from rbu.celery import app
from statuses.views import import_one_csv

from rbu import settings


@app.task(name="sum_two_numbers")
def add(x, y):
    print(x + y)
    return x + y


@app.task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total


@app.task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)


@app.task(name="task_import_csv")
def task_import():
    import_one_csv()
    return True

