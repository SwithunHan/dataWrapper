# Generated by Django 2.1.7 on 2019-04-22 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hisprice',
            name='houseAD',
            field=models.CharField(default='', max_length=10),
        ),
    ]