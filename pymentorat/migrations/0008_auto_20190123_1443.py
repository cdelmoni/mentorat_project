# Generated by Django 2.1.5 on 2019-01-23 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pymentorat', '0007_auto_20190120_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='id_OD',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]