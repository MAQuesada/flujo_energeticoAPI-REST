# Generated by Django 4.1.2 on 2022-11-19 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("transporte_app", "0006_rename_desc_articulo_descripcion_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="resultado",
            unique_together={("mes", "anno", "articulo")},
        ),
    ]