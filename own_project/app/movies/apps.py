from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
    verbose_name = _('verbose_name')

    def ready(self):
        import movies.signals
