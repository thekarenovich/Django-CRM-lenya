# Generated by Django 5.0.1 on 2024-02-25 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_drysubstancetype_fermenttype_primertype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drysubstancetype',
            name='reagent',
            field=models.FloatField(verbose_name='Код реагента'),
        ),
        migrations.AlterField(
            model_name='fermenttype',
            name='reagent',
            field=models.FloatField(verbose_name='Код реагента'),
        ),
        migrations.AlterField(
            model_name='primertype',
            name='reagent',
            field=models.FloatField(verbose_name='Код реагента'),
        ),
        migrations.AlterField(
            model_name='restrictionenzymetype',
            name='reagent',
            field=models.FloatField(verbose_name='Код реагента'),
        ),
        migrations.AlterField(
            model_name='substancesolutiontype',
            name='reagent',
            field=models.FloatField(verbose_name='Код реагента'),
        ),
    ]