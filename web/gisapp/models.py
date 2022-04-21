from django.db import models


class GeoObject(models.Model):
    layer_name = models.CharField(null=True, blank=True, max_length=150, unique=True, verbose_name="Название слоя в GeoServer")
    lat = models.FloatField(null=True, blank=True, verbose_name="Широта")
    lon = models.FloatField(null=True, blank=True, verbose_name="Долгота")
    zoom_level = models.FloatField(null=True, blank=True, verbose_name="Уровень Zoomа")

    class Meta:
        abstract = True


class Region(GeoObject):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Область"
        verbose_name_plural = "Области"

    def __str__(self):
        return f"{self.name}"


class District(GeoObject):
    region = models.ForeignKey('Region', on_delete=models.PROTECT, verbose_name="Область")
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"

    def __str__(self):
        return f"Район {self.name} в {self.region}"


class Town(GeoObject):
    district = models.ForeignKey('District', on_delete=models.PROTECT, verbose_name="Район")
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Населённый пункт"
        verbose_name_plural = "Населённые пункты"

    def __str__(self):
        return f"Населённый пункт {self.name} в {self.district}"


class Hospital(GeoObject):
    town = models.ForeignKey('Town', on_delete=models.PROTECT, verbose_name="Населённый пункт")
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    service_types = models.ManyToManyField('ServiceType', verbose_name="Типы услуг")
    equipments = models.ManyToManyField('EquipmentType', verbose_name="Оборудование", through="EquipmentHospital")

    fundings = models.ManyToManyField('FundingSource', verbose_name="Финансирование", through="Funding")
    expenses = models.ManyToManyField('ExpensesPurpose', verbose_name="Расходы", through="Expense")

    address = models.CharField(max_length=250, verbose_name="Адрес")

    number_of_doctors_with_category = models.PositiveSmallIntegerField(verbose_name="Количество врачей с категорией")
    number_of_doctors_without_category = models.PositiveSmallIntegerField(verbose_name="Количество врачей без категории")
    average_yearly_employees = models.FloatField(verbose_name="Среднегодовая численность работников")

    area = models.FloatField(verbose_name="Площадь")
    number_of_bed_places = models.PositiveSmallIntegerField(verbose_name="Количество койкомест")

    clinical_rating_fb = models.FloatField(verbose_name="Клинический рейтинг ФБ")
    clinical_rating_kr = models.FloatField(verbose_name="Клинический рейтинг КР")
    clinical_rating_max = models.FloatField(verbose_name="Клинический рейтинг max")
    clinical_rating_stars = models.FloatField(verbose_name="Клинический рейтинг - Звёзды")

    management_rating_fb = models.FloatField(verbose_name="Рейтинг по показателям менеджмента ФБ")
    management_rating_kr = models.FloatField(verbose_name="Рейтинг по показателям менеджмента КР")
    management_rating_max = models.FloatField(verbose_name="Рейтинг по показателям менеджмента max")
    management_rating_stars = models.FloatField(verbose_name="Рейтинг по показателям менеджмента - Звёзды")

    number_of_patients_yearly = models.PositiveIntegerField(verbose_name="Количество пациентов за год")
    male_patients_ratio = models.FloatField(verbose_name="Доля пациентов-мужчин")
    female_patients_ratio = models.FloatField(verbose_name="Доля пациентов-женщин")
    patients_average_stay_days = models.FloatField(verbose_name="Среднее время пребывания пациентов")

    class Meta:
        verbose_name = "Больница"
        verbose_name_plural = "Больницы"

    def __str__(self):
        return f"Больница {self.name} в {self.town}"


class ServiceType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Тип услуги")

    class Meta:
        verbose_name = "Тип услуги"
        verbose_name_plural = "Типы услуг"

    def __str__(self):
        return f"Тип услуги {self.name}"


class EquipmentType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Тип оборудования")

    class Meta:
        verbose_name = "Тип оборудования"
        verbose_name_plural = "Типы оборудования"

    def __str__(self):
        return f"Тип оборудования {self.name}"


class EquipmentHospital(models.Model):
    equipment = models.ForeignKey("EquipmentType", verbose_name="Оборудование", on_delete=models.PROTECT)
    hospital = models.ForeignKey("Hospital", verbose_name="Больница", on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Связь Больница-Оборудование"
        verbose_name_plural = "Связи Больница-Оборудование"
        unique_together = ('equipment', 'hospital')

    def __str__(self):
        return f"Связь Больница-Оборудование {self.hospital} - {self.equipment} ({self.quantity}шт.)"


class FundingSource(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Источник финансирования"
        verbose_name_plural = "Источники финансирования"

    def __str__(self):
        return f"Источник финансирования {self.name}"


class Funding(models.Model):
    funding_source = models.ForeignKey("FundingSource", verbose_name="Источник финансирования", on_delete=models.PROTECT)
    hospital = models.ForeignKey("Hospital", verbose_name="Больница", on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(verbose_name="Объём (тг)")

    class Meta:
        verbose_name = "Связь Больница-Финансирование"
        verbose_name_plural = "Связи Больница-Финансирование"
        unique_together = ('funding_source', 'hospital')

    def __str__(self):
        return f"Связь Больница-Источник Финансирования {self.hospital} - {self.funding_source} ({self.amount}тг.)"


class ExpensesPurpose(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Цель расходов"
        verbose_name_plural = "Цели расходов"

    def __str__(self):
        return f"Цель расходов {self.name}"


class Expense(models.Model):
    expenses_purpose = models.ForeignKey("ExpensesPurpose", verbose_name="Цель расхода", on_delete=models.PROTECT)
    hospital = models.ForeignKey("Hospital", verbose_name="Больница", on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(verbose_name="Объём (тг)")

    class Meta:
        verbose_name = "Связь Больница-Расход"
        verbose_name_plural = "Связи Больница-Расход"
        unique_together = ('expenses_purpose', 'hospital')

    def __str__(self):
        return f"Связь Больница-Расход {self.hospital} - {self.expenses_purpose} ({self.amount}тг.)"
