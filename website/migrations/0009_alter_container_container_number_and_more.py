# Generated by Django 5.0.1 on 2024-02-25 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_containertype_storagechamber_container_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='container_number',
            field=models.IntegerField(max_length=50, verbose_name='Номер контейнера'),
        ),
        migrations.AlterField(
            model_name='container',
            name='reagent_number',
            field=models.IntegerField(verbose_name='Номер реагента'),
        ),
        migrations.AlterField(
            model_name='reagent',
            name='reagent_number',
            field=models.IntegerField(max_length=50, verbose_name='Номер реагента'),
        ),
    ]