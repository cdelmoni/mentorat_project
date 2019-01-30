# Generated by Django 2.1.5 on 2019-01-30 21:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pymentorat', '0014_auto_20190130_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='begin_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date de début'),
        ),
        migrations.AlterField(
            model_name='eda',
            name='inscription_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name="Date d'inscription"),
        ),
        migrations.AlterField(
            model_name='mentor',
            name='inscription_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name="Date d'inscription"),
        ),
    ]
