from __future__ import annotations

from typing import Optional

from django.db import models
from django.urls import reverse, NoReverseMatch


class Menu(models.Model):
    """
    Модель меню с древовидной структурой.
    """

    name = models.CharField(max_length=100, unique=True, verbose_name="Название меню")

    class Meta:
        ordering = ("name",)
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self) -> str:
        return self.name


class MenuItem(models.Model):
    """
    Элемент меню. Поддерживает иерархию через parent.
    """

    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Меню",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
        verbose_name="Родительский элемент",
    )
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    url = models.CharField("URL", max_length=500, blank=True)
    named_url = models.CharField("Именованный URL", max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ("order", "id")
        constraints = [
            models.CheckConstraint(
                check=(~models.Q(url="") | ~models.Q(named_url="")),
                name="menu_item_has_some_url",
            )
        ]
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

    def __str__(self) -> str:
        return f"{self.title} ({self.menu.name})"

    def get_absolute_url(self) -> str:
        """
        Возвращает URL для перехода по элементу меню.
        """
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                pass
        return self.url or "#"

    def is_ancestor_of(self, other: "MenuItem") -> bool:
        """
        Возвращает True, если текущий элемент является предком другого элемента.
        """
        current: Optional["MenuItem"] = other.parent
        while current is not None:
            if current == self:
                return True
            current = current.parent
        return False
