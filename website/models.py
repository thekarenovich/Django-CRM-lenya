from django.db import models
from django.contrib.auth.models import User


class ReagentType(models.Model):
    code = models.CharField(max_length=50, verbose_name="Код типа")
    name = models.CharField(max_length=100, verbose_name="Наименование типа")

    def __str__(self):
        return self.name


class ContainerType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование типа контейнера")

    def __str__(self):
        return self.name


class StorageChamber(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование камеры")
    shelf_number = models.IntegerField(verbose_name="Номер полки")

    def __str__(self):
        return self.name


class StorageLocation(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование местоположения")
    chamber = models.ForeignKey(StorageChamber, on_delete=models.CASCADE, verbose_name="ID камеры")

    def __str__(self):
        return self.name


class Container(models.Model):
    container_number = models.CharField(max_length=50, verbose_name="Номер контейнера")
    location = models.ForeignKey(StorageLocation, on_delete=models.CASCADE, verbose_name="Местоположение контейнера")
    container_type = models.ForeignKey(ContainerType, on_delete=models.CASCADE, verbose_name="Тип контейнера")
    reagent_quantity = models.IntegerField(verbose_name="Количество реагента")

    def __str__(self):
        return self.container_number


class Reagent(models.Model):
    reagent_number = models.IntegerField(verbose_name="Номер реагента")
    reagent_name = models.CharField(max_length=100, verbose_name="Наименование реагента")
    container_number = models.ForeignKey(Container, on_delete=models.CASCADE, verbose_name="Номер контейнера")
    quantity = models.IntegerField(verbose_name="Количество реагента")
    reagent_type = models.ForeignKey(ReagentType, on_delete=models.CASCADE, verbose_name="Тип реагента")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    expiration_date = models.DateField(verbose_name="Срок годности")
    storage_temperature = models.IntegerField(verbose_name="Температура хранения")
    description = models.TextField(verbose_name="Описание")
    special_instructions = models.TextField(verbose_name="Особые указания")
    last_usage = models.DateTimeField(null=True, blank=True, verbose_name="Последнее использование")
    last_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name="Последний пользователь")

    def __str__(self):
        return self.reagent_name


class Magazine(models.Model):
    number = models.CharField(max_length=50, verbose_name="Номер журнала")
    reagent_number = models.ForeignKey(Reagent, on_delete=models.CASCADE, verbose_name="Номер реагента")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    content = models.TextField(verbose_name="Содеражние")
    last_alert = models.DateTimeField(null=True, blank=True, verbose_name="Последнее изменение")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name="Автор")


# type 1
class OtherSolution(models.Model):
    reagent = models.FloatField(verbose_name="Код реагента")
    component_concentration = models.FloatField(verbose_name="Концентрация составляющих веществ")
    molarity = models.FloatField(verbose_name="Молярность раствора")
    ph = models.FloatField(verbose_name="Х раствора")
    reagent_type = models.ForeignKey(ReagentType, on_delete=models.CASCADE, verbose_name="Код типа")


# type 2
class BufferSolution(models.Model):
    reagent = models.FloatField(verbose_name="Код реагента")
    component_concentration = models.FloatField(verbose_name="Концентрация составляющих веществ")
    molarity = models.FloatField(verbose_name="Молярность раствора")
    ph = models.FloatField(verbose_name="Х раствора")
    reagent_type = models.ForeignKey(ReagentType, on_delete=models.CASCADE, verbose_name="Код типа")


# type 3
class FermentType(models.Model):
    reagent = models.FloatField(verbose_name="Код реагента")
    class_name = models.CharField(max_length=100, verbose_name="Класс фермента")
    activity_per_ml = models.FloatField(verbose_name="Ед активности / мл")
    optimal_temperature = models.IntegerField(verbose_name="Оптимальная температура")
    deactivation_capability = models.CharField(max_length=100, verbose_name="Возможность дезактивации")
    storage_buffer_type = models.CharField(max_length=100, verbose_name="Тип буфера хранения")
    reaction_buffer = models.CharField(max_length=100, verbose_name="Реакционный буфер")
    source = models.CharField(max_length=100, verbose_name="Источник")
    reagent_type = models.ForeignKey(ReagentType, on_delete=models.CASCADE, verbose_name="Код типа")


# type 4
class DrySubstanceType(models.Model):
    reagent = models.FloatField(verbose_name="Код реагента")
    supplier = models.CharField(max_length=100, verbose_name="Поставщик")
    purity = models.FloatField(verbose_name="Чистота")
    applications = models.TextField(verbose_name="Допустимые применения")
    reagent_type = models.ForeignKey(ReagentType, on_delete=models.CASCADE, verbose_name="Код типа")


# type 5
class PrimerType(models.Model):
    reagent = models.FloatField(verbose_name="Код реагента")
    sequence = models.TextField(verbose_name="Последовательность")
    annealing_temperature = models.IntegerField(verbose_name="Температура отжига")
    composition_for_annealing_temperature = models.CharField(max_length=100,
                                                             verbose_name="Состав смеси для температуры отжига")
    concentration = models.FloatField(verbose_name="Концентрация")
    length = models.IntegerField(verbose_name="Длина праймера")
    reagent_type = models.ForeignKey(ReagentType, on_delete=models.CASCADE, verbose_name="Код типа")


# type 6
class RestrictionEnzymeType(models.Model):
    reagent = models.FloatField(verbose_name="Код реагента")
    activity_percentage_in_buffers = models.FloatField(verbose_name="% активности в буферах")
    activity_per_ml = models.FloatField(verbose_name="Ед активности / мл")
    optimal_temperature = models.IntegerField(verbose_name="Оптимальная температура")
    deactivation_capability = models.CharField(max_length=100, verbose_name="Возможность дезактивации")
    storage_buffer_type = models.CharField(max_length=100, verbose_name="Тип буфера хранения")
    reaction_buffer = models.CharField(max_length=100, verbose_name="Реакционный буфер")
    restriction_site = models.CharField(max_length=100, verbose_name="Сайт рестрикции")
    reagent_type = models.ForeignKey(ReagentType, on_delete=models.CASCADE, verbose_name="Код типа")


# type 7
class SubstanceSolutionType(models.Model):
    reagent = models.FloatField(verbose_name="Код реагента")
    dry_reagent = models.CharField(max_length=100, verbose_name="Сухой реагент")
    dry_reagent_quantity = models.FloatField(verbose_name="Количество сухого реагента")
    concentration = models.FloatField(verbose_name="Концентрация")
    solvent = models.CharField(max_length=100, verbose_name="Растворитель")
    reagent_type = models.ForeignKey(ReagentType, on_delete=models.CASCADE, verbose_name="Код типа")
