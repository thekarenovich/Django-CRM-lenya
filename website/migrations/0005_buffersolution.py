# Generated by Django 5.0.1 on 2024-02-24 22:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_othersolution_reagent'),
    ]

    operations = [
        migrations.CreateModel(
            name='BufferSolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reagent', models.FloatField(verbose_name='Код реагента')),
                ('component_concentration', models.FloatField(verbose_name='Концентрация составляющих веществ')),
                ('molarity', models.FloatField(verbose_name='Молярность раствора')),
                ('ph', models.FloatField(verbose_name='Х раствора')),
                ('reagent_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.reagenttype', verbose_name='Код типа')),
            ],
        ),
    ]