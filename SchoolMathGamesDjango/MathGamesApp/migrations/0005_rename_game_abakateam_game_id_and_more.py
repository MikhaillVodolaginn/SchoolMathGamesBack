# Generated by Django 4.2.1 on 2023-05-29 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("MathGamesApp", "0004_rename_game_id_abakateam_game_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="abakateam",
            old_name="game",
            new_name="game_id",
        ),
        migrations.RenameField(
            model_name="bonusteam",
            old_name="game",
            new_name="game_id",
        ),
        migrations.RenameField(
            model_name="dominoteam",
            old_name="game",
            new_name="game_id",
        ),
    ]