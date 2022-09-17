# Generated by Django 4.1.1 on 2022-09-17 08:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Messages",
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
                ("creation_date", models.DateField(auto_now_add=True)),
                ("creation_time", models.TimeField(auto_now_add=True)),
                (
                    "content",
                    models.TextField(
                        validators=[django.core.validators.MaxLengthValidator(700)]
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="message_creator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Thread",
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
                ("subject", models.CharField(blank=True, default="", max_length=50)),
                ("creation_date", models.DateField(auto_now_add=True)),
                ("creation_time", models.TimeField(auto_now_add=True)),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="thread_creator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "messages",
                    models.ManyToManyField(
                        blank=True,
                        related_name="thread_messages",
                        to="cars_communicator_app.messages",
                    ),
                ),
                (
                    "second_person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="thread_second_person",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RegisteredCars",
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
                ("brand", models.CharField(max_length=50)),
                ("model", models.CharField(max_length=50)),
                ("registration_date", models.DateField(auto_now_add=True)),
                ("registration_time", models.TimeField(auto_now_add=True)),
                ("registration_number", models.CharField(max_length=10)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="registeredcars_creator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="messages",
            name="thread",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="messages_thread",
                to="cars_communicator_app.thread",
            ),
        ),
    ]