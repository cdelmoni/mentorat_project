# Generated by Django 2.1.5 on 2019-01-28 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pymentorat', '0010_auto_20190123_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='id_OD',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]