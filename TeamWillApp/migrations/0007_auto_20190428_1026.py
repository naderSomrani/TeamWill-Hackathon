# Generated by Django 2.2 on 2019-04-28 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamWillApp', '0006_dosecheance'),
    ]

    operations = [
        migrations.CreateModel(
            name='DOSSIER',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DOSID', models.IntegerField()),
                ('DOSCAPITAL', models.FloatField()),
                ('DOSNBRECHEANCE', models.IntegerField()),
                ('DOSCAPITALRESTANT', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='prospect',
            name='PROAGE',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='prospect',
            name='PRODIRIGENT',
            field=models.CharField(default='Dirigent', max_length=100),
        ),
        migrations.AddField(
            model_name='prospect',
            name='PROFONCTION',
            field=models.CharField(default='Salarie', max_length=100),
        ),
        migrations.AddField(
            model_name='prospect',
            name='PRONBRENFANT',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='prospect',
            name='PROSALAIRE',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='prospect',
            name='PROSECTEURFONCTION',
            field=models.CharField(default='Public', max_length=100),
        ),
        migrations.AddField(
            model_name='prospect',
            name='PROSITUATIONFAMILLE',
            field=models.CharField(default='Marie', max_length=50),
        ),
    ]
