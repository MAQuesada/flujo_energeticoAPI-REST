# Generated by Django 4.1.2 on 2022-11-18 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "transporte_app",
            "0003_articulo_resolucion_alter_vehiculo_prueba_litro_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="articulo",
            name="desc",
            field=models.CharField(default="", max_length=200),
        ),
    ]