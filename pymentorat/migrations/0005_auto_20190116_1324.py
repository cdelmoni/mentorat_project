# Generated by Django 2.1.5 on 2019-01-16 12:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pymentorat', '0004_auto_20190116_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='convocation',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Heure du rendez-vous'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='convocation',
            name='date',
            field=models.DateField(verbose_name='Date de rendez-vous'),
        ),
    ]