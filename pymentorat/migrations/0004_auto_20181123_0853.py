# Generated by Django 2.1.3 on 2018-11-23 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pymentorat', '0003_auto_20181123_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='portable',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='student',
            name='tel',
            field=models.CharField(max_length=13),
        ),
    ]
