from django.apps import AppConfig


class UnloadAppConfig(AppConfig):
    name = 'unloads'
    verbose_name = "Выгрузки"  # А здесь, имя которое необходимо отобразить в админке
