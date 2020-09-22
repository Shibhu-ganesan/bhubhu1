from django.apps import AppConfig

class DennisappConfig(AppConfig):
    name = 'dennisapp'

    def ready(self):
        import dennisapp.signals
