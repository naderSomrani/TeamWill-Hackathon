# Generated by Django 2.2 on 2019-04-28 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChampCredit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CCRCODE', models.CharField(max_length=100)),
                ('CCRNOM', models.CharField(max_length=100)),
                ('CCRTYPE', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DocCredit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DCRCODE', models.CharField(max_length=100)),
                ('DCRNOM', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DOSSIERPROSPECT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DPRCODE', models.CharField(max_length=100)),
                ('DPRCAPITAL', models.FloatField()),
                ('DPRTAUXINTERET', models.FloatField()),
                ('DPRTOTALINTERET', models.FloatField()),
                ('DPRMENSUALITE', models.CharField(max_length=100)),
                ('DPRNBRECHEANCE', models.FloatField()),
                ('DPRECHEANCE', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PROSPECT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PRONOM', models.CharField(max_length=100)),
                ('PROPRENOM', models.CharField(max_length=100)),
                ('PRODEPRENOM', models.CharField(max_length=100)),
                ('PROMAIL', models.CharField(max_length=100, unique=True)),
                ('PROTEL', models.CharField(max_length=20)),
                ('PRODATENAISS', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TypeCredit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TCRCODE', models.CharField(max_length=100)),
                ('TCRNOM', models.CharField(max_length=100)),
                ('TCRTAUXINTERT', models.FloatField()),
                ('TCRDUREEMAX', models.IntegerField()),
                ('TCRMAXCAPITAL', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LKTCRDOC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DCRID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TeamWillApp.DocCredit')),
                ('TCRID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TeamWillApp.TypeCredit')),
            ],
        ),
        migrations.CreateModel(
            name='LKTCRCHAMP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CCRID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TeamWillApp.ChampCredit')),
                ('TCRID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TeamWillApp.TypeCredit')),
            ],
        ),
        migrations.CreateModel(
            name='DPRECHEANCE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DPRORDER', models.IntegerField()),
                ('DPRINTERETN', models.FloatField()),
                ('DPRCAPITALN', models.FloatField()),
                ('DPRECHEANCEN', models.FloatField()),
                ('DPRDATE', models.DateField()),
                ('DPRID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TeamWillApp.DOSSIERPROSPECT')),
            ],
        ),
        migrations.CreateModel(
            name='DPRCCRVALEUR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VALEUR', models.CharField(max_length=100)),
                ('CCRID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TeamWillApp.ChampCredit')),
                ('DPRID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TeamWillApp.DOSSIERPROSPECT')),
            ],
        ),
        migrations.AddField(
            model_name='dossierprospect',
            name='PROCODE',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TeamWillApp.PROSPECT'),
        ),
        migrations.CreateModel(
            name='DOCUMENTDEMANDE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DCRCODE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TeamWillApp.DocCredit')),
            ],
        ),
        migrations.CreateModel(
            name='DEMANDECREDIT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DemCode', models.IntegerField()),
                ('DPRID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TeamWillApp.DOSSIERPROSPECT')),
            ],
        ),
    ]
