from django.apps import AppConfig


class UnloadAppConfig(AppConfig):
    name = 'unload'
    verbose_name = "Выгрузки"  # А здесь, имя которое необходимо отобразить в админке
