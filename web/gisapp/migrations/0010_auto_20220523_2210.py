# Generated by Django 2.2.13 on 2022-05-23 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gisapp', '0009_auto_20220523_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientstay',
            name='case_id',
            field=models.PositiveIntegerField(default=0, verbose_name='ID случая'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patientstay',
            name='diagnosis',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Диагноз заключительный'),
        ),
        migrations.AddField(
            model_name='patientstay',
            name='diagnosis_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Основное'), (1, 'Сопутствующее'), (2, 'Уточняющее')], default=0, verbose_name='Вид диагноза'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patientstay',
            name='is_diagnosis_final',
            field=models.BooleanField(default=True, verbose_name='Заключительный ли диагноз'),
        ),
    ]