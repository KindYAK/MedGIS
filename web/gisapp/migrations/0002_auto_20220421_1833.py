# Generated by Django 2.2.13 on 2022-04-21 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gisapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='address',
            field=models.CharField(default='', max_length=250, verbose_name='Адрес'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='area',
            field=models.FloatField(default=0, verbose_name='Площадь'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='average_yearly_employees',
            field=models.FloatField(default=0, verbose_name='Среднегодовая численность работников'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='clinical_rating_fb',
            field=models.FloatField(default=0, verbose_name='Клинический рейтинг ФБ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='clinical_rating_kr',
            field=models.FloatField(default=0, verbose_name='Клинический рейтинг КР'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='clinical_rating_max',
            field=models.FloatField(default=0, verbose_name='Клинический рейтинг max'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='clinical_rating_stars',
            field=models.FloatField(default=0, verbose_name='Клинический рейтинг - Звёзды'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='female_patients_ratio',
            field=models.FloatField(default=0, verbose_name='Доля пациентов-женщин'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='male_patients_ratio',
            field=models.FloatField(default=0, verbose_name='Доля пациентов-мужчин'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='management_rating_fb',
            field=models.FloatField(default=0, verbose_name='Рейтинг по показателям менеджмента ФБ'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='management_rating_kr',
            field=models.FloatField(default=0, verbose_name='Рейтинг по показателям менеджмента КР'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='management_rating_max',
            field=models.FloatField(default=0, verbose_name='Рейтинг по показателям менеджмента max'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='management_rating_stars',
            field=models.FloatField(default=0, verbose_name='Рейтинг по показателям менеджмента - Звёзды'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='number_of_bed_places',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Количество койкомест'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='number_of_doctors_with_category',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Количество врачей с категорией'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='number_of_doctors_without_category',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Количество врачей без категории'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='number_of_patients_yearly',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество пациентов за год'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hospital',
            name='patients_average_stay_days',
            field=models.FloatField(default=0, verbose_name='Среднее время пребывания пациентов'),
            preserve_default=False,
        ),
    ]
