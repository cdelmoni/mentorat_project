# Generated by Django 2.1.2 on 2019-01-05 15:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pymentorat', '0005_auto_20181123_0902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('begin_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('contrat_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pymentorat.Contrat')),
            ],
            options={
                'verbose_name': 'Contrat',
                'verbose_name_plural': 'Contrats',
            },
        ),
        migrations.AlterModelOptions(
            name='discipline',
            options={'verbose_name': 'Discipline', 'verbose_name_plural': 'Disciplines'},
        ),
        migrations.AlterModelOptions(
            name='eda',
            options={'verbose_name': "Elève demandeur d'aide", 'verbose_name_plural': "Elèves demandeurs d'aide"},
        ),
        migrations.AlterModelOptions(
            name='mentor',
            options={'verbose_name': 'Elève mentor', 'verbose_name_plural': 'Elèves mentors'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Elève', 'verbose_name_plural': 'Elèves'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': 'Maître', 'verbose_name_plural': 'Maîtres'},
        ),
        migrations.AddField(
            model_name='discipline',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='discipline',
            name='modification_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='eda',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eda',
            name='modification_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='mentor',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mentor',
            name='modification_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='student',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='modification_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='modification_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='contrat',
            name='discipline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pymentorat.Discipline'),
        ),
        migrations.AddField(
            model_name='contrat',
            name='eda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pymentorat.EDA'),
        ),
        migrations.AddField(
            model_name='contrat',
            name='mentor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pymentorat.Mentor'),
        ),
    ]
