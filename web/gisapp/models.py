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

    # ...

    class Meta:
        verbose_name = "Больница"
        verbose_name_plural = "Больницы"

    def __str__(self):
        return f"Больница {self.name} в {self.town}"
