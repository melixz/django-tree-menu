from django.apps import AppConfig


class MenuConfig(AppConfig):
    """
    Конфиг приложения древовидного меню.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "django-tree-menu.menu"
    verbose_name = "Древовидное меню"
