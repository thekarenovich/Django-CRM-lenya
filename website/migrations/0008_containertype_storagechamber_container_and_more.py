# Generated by Django 5.0.1 on 2024-02-25 13:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_alter_drysubstancetype_reagent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContainerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование типа контейнера')),
            ],
        ),
        migrations.CreateModel(
            name='StorageChamber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование камеры')),
                ('shelf_number', models.IntegerField(verbose_name='Номер полки')),
            ],
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('container_number', models.CharField(max_length=50, verbose_name='Номер контейнера')),
                ('reagent_quantity', models.IntegerField(verbose_name='Количество реагента')),
                ('reagent_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.reagent', verbose_name='Номер реагента')),
                ('container_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.containertype', verbose_name='Тип контейнера')),
            ],
        ),
        migrations.AlterField(
            model_name='reagent',
            name='container_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.container', verbose_name='Номер контейнера'),
        ),
        migrations.CreateModel(
            name='StorageLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование местоположения')),
                ('chamber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.storagechamber', verbose_name='ID камеры')),
            ],
        ),
        migrations.AddField(
            model_name='container',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.storagelocation', verbose_name='Местоположение контейнера'),
        ),
    ]