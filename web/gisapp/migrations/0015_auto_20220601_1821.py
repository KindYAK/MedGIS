# Generated by Django 2.2.13 on 2022-06-01 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gisapp', '0014_auto_20220601_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizenship',
            name='name',
            field=models.CharField(max_length=500, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='ethnicity',
            name='name',
            field=models.CharField(max_length=500, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(max_length=500, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='stayprofile',
            name='name',
            field=models.CharField(max_length=500, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='surgerytype',
            name='code',
            field=models.CharField(max_length=500, unique=True, verbose_name='Код'),
        ),
        migrations.AlterField(
            model_name='surgerytype',
            name='name',
            field=models.CharField(max_length=500, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='town',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Название'),
        ),
    ]