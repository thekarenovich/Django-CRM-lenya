# Generated by Django 5.0.1 on 2024-02-24 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_reagenttype_othersolution_alter_reagent_reagent_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='othersolution',
            name='reagent',
            field=models.FloatField(verbose_name='Код реагента'),
        ),
    ]
