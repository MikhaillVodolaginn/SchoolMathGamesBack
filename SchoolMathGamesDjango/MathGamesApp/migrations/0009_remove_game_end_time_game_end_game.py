# Generated by Django 4.2.1 on 2023-05-30 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("MathGamesApp", "0008_game_end_time"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="game",
            name="end_time",
        ),
        migrations.AddField(
            model_name="game",
            name="end_game",
            field=models.IntegerField(default=0),
        ),
    ]
