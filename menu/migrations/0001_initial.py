# Generated by Django 5.2.3 on 2025-06-17 17:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Menu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Название меню"
                    ),
                ),
            ],
            options={
                "verbose_name": "Меню",
                "verbose_name_plural": "Меню",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="MenuItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Заголовок")),
                (
                    "url",
                    models.CharField(blank=True, max_length=500, verbose_name="URL"),
                ),
                (
                    "named_url",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Именованный URL"
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(default=0, verbose_name="Порядок"),
                ),
                (
                    "menu",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="menu.menu",
                        verbose_name="Меню",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="menu.menuitem",
                        verbose_name="Родительский элемент",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пункт меню",
                "verbose_name_plural": "Пункты меню",
                "ordering": ("order", "id"),
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(
                            models.Q(("url", ""), _negated=True),
                            models.Q(("named_url", ""), _negated=True),
                            _connector="OR",
                        ),
                        name="menu_item_has_some_url",
                    )
                ],
            },
        ),
    ]
