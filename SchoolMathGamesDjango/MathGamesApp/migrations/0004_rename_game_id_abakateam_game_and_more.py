# Generated by Django 4.2.1 on 2023-05-28 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "MathGamesApp",
            "0003_alter_dominoteam_point0_alter_dominoteam_point1_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="abakateam",
            old_name="game_id",
            new_name="game",
        ),
        migrations.RenameField(
            model_name="bonusteam",
            old_name="game_id",
            new_name="game",
        ),
        migrations.RenameField(
            model_name="dominoteam",
            old_name="game_id",
            new_name="game",
        ),
    ]
