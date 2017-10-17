from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Cement


class CementAdmin(ModelAdmin):
    # навигация по датам из этого поля
    date_hierarchy = 'date'
    # Поля выводимые в списке объектов
    list_display = (
        'date',
        'value',
    )

    class Meta:
        model = Cement


admin.site.register(Cement, CementAdmin)
