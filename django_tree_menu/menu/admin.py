from __future__ import annotations

from django.contrib import admin

from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    """
    Вспомогательный класс для отображения элементов меню внутри меню.
    """

    model = MenuItem
    extra = 1
    fields = ("title", "parent", "url", "named_url", "order")
    autocomplete_fields = ("parent",)
    ordering = ("order", "id")


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """
    Админка для меню. Позволяет редактировать элементы меню.
    """

    list_display = ("name",)
    inlines = (MenuItemInline,)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """
    Админка для элементов меню.
    """

    list_display = ("title", "menu", "parent", "order")
    list_select_related = ("menu", "parent")
    list_filter = ("menu",)
    search_fields = ("title",)
    ordering = ("menu__name", "parent__id", "order", "id")
