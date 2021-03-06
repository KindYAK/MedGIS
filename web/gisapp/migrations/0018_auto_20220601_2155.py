# Generated by Django 2.2.13 on 2022-06-01 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gisapp', '0017_auto_20220601_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisapp.Region', verbose_name='Область'),
        ),
        migrations.AlterField(
            model_name='equipmenthospital',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisapp.EquipmentType', verbose_name='Оборудование'),
        ),
        migrations.AlterField(
            model_name='equipmenthospital',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisapp.Hospital', verbose_name='Больница'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='expenses_purpose',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisapp.ExpensesPurpose', verbose_name='Цель расхода'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisapp.Hospital', verbose_name='Больница'),
        ),
        migrations.AlterField(
            model_name='funding',
            name='funding_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisapp.FundingSource', verbose_name='Источник финансирования'),
        ),
        migrations.AlterField(
            model_name='funding',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisapp.Hospital', verbose_name='Больница'),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='town',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gisapp.Town', verbose_name='Населённый пункт'),
        ),
        migrations.AlterField(
            model_name='mkbclass',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gisapp.MKBClass'),
        ),
        migrations.AlterField(
            model_name='patientstay',
            name='citizenship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisapp.Citizenship', verbose_name='Гражданство'),
        ),
        migrations.AlterField(
            model_name='patientstay',
            name='diagnosis_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Основное'), (1, 'Сопутствующее'), (2, 'Уточняющее'), (3, 'Осложнение')], verbose_name='Вид диагноза'),
        ),
        migrations.AlterField(
            model_name='patientstay',
            name='ethnicity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisapp.Ethnicity', verbose_name='Этнос'),
        ),
        migrations.AlterField(
            model_name='patientstay',
            name='fix_hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fix_hospital', to='gisapp.Hospital', verbose_name='Больница прикрепления'),
        ),
        migrations.AlterField(
            model_name='patientstay',
            name='from_hospital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_hospital', to='gisapp.Hospital', verbose_name='Больница откуда направили'),
        ),
        migrations.AlterField(
            model_name='patientstay',
            name='funding_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisapp.FundingSource', verbose_name='Источник финансирования'),
        ),
        migrations.AlterField(
            model_name='patientstay',
            name='hospital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisapp.Hospital', verbose_name='Больница'),
        ),
        migrations.AlterField(
            model_name='patientstay',
            name='mkb',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisapp.MKBClass', verbose_name='Класс МКБ'),
        ),
        migrations.AlterField(
            model_name='patientstay',
            name='mkb_complication',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mbk_complication', to='gisapp.MKBClass', verbose_name='Осложнение - Класс МКБ'),
        ),
        migrations.AlterField(
            model_name='patientstay',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisapp.StayProfile', verbose_name='Профиль'),
        ),
        migrations.AlterField(
            model_name='patientstay',
            name='surgery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gisapp.SurgeryType', verbose_name='Тип операции'),
        ),
        migrations.AlterField(
            model_name='town',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisapp.District', verbose_name='Район'),
        ),
    ]
