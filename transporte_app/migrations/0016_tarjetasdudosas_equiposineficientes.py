# Generated by Django 4.1.2 on 2022-11-27 17:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("transporte_app", "0015_rename_dif_consumo_equipoequipo_dif_consumo_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tarjetasdudosas",
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
                    "mes",
                    models.IntegerField(
                        choices=[
                            (1, "Enero"),
                            (2, "Febrero"),
                            (3, "Marzo"),
                            (4, "Abril"),
                            (5, "Mayo"),
                            (6, "Junio"),
                            (7, "Julio"),
                            (8, "Agosto"),
                            (9, "Septiembre"),
                            (10, "Octubre"),
                            (11, "Noviembre"),
                            (12, "Diciembre"),
                        ]
                    ),
                ),
                (
                    "anno",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(2020),
                            django.core.validators.MaxValueValidator(2100),
                        ]
                    ),
                ),
                ("nro_tarjeta", models.CharField(max_length=20)),
                ("servicio", models.CharField(max_length=200)),
                ("causa", models.CharField(blank=True, default="", max_length=200)),
                ("medidas", models.CharField(blank=True, default="", max_length=200)),
                (
                    "matricula_tarjeta",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="t_matricula_tarjeta",
                        to="transporte_app.vehiculo",
                    ),
                ),
            ],
            options={
                "ordering": ["matricula_tarjeta"],
                "unique_together": {("mes", "anno", "matricula_tarjeta")},
            },
        ),
        migrations.CreateModel(
            name="EquiposIneficientes",
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
                    "mes",
                    models.IntegerField(
                        choices=[
                            (1, "Enero"),
                            (2, "Febrero"),
                            (3, "Marzo"),
                            (4, "Abril"),
                            (5, "Mayo"),
                            (6, "Junio"),
                            (7, "Julio"),
                            (8, "Agosto"),
                            (9, "Septiembre"),
                            (10, "Octubre"),
                            (11, "Noviembre"),
                            (12, "Diciembre"),
                        ]
                    ),
                ),
                (
                    "anno",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(2020),
                            django.core.validators.MaxValueValidator(2100),
                        ]
                    ),
                ),
                ("servicio", models.CharField(max_length=200)),
                ("comb_sin_respaldo", models.FloatField()),
                ("medidas", models.CharField(blank=True, default="", max_length=200)),
                (
                    "matricula_ineficiente",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="t_matricula_ineficiente",
                        to="transporte_app.vehiculo",
                    ),
                ),
            ],
            options={
                "ordering": ["matricula_ineficiente"],
                "unique_together": {("mes", "anno", "matricula_ineficiente")},
            },
        ),
    ]