# Generated by Django 3.0.5 on 2021-05-03 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('age', models.IntegerField()),
                ('designation', models.CharField(max_length=256)),
            ],
        ),
    ]
