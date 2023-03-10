# Generated by Django 4.1.2 on 2022-11-22 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transporte_app", "0011_vehiculo_chofer_alter_tarjetas_chat_pr_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tikets",
            name="cantidad_entrada",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tikets",
            name="cantidad_saldo",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tikets",
            name="cantidad_salida",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tikets",
            name="importe_entrada",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tikets",
            name="importe_saldo",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tikets",
            name="importe_salida",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tikets",
            name="lugar",
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="tikets",
            name="nro_chip",
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
