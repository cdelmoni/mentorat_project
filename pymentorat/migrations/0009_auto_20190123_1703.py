# Generated by Django 2.1.5 on 2019-01-23 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pymentorat', '0008_auto_20190123_1443'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='current_classe',
            new_name='classe',
        ),
    ]
