# Generated by Django 3.0.6 on 2020-12-08 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersreal',
            name='user_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name=11),
        ),
    ]
