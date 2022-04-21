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
