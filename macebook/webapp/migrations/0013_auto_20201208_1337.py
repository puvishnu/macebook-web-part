# Generated by Django 3.0.6 on 2020-12-08 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_auto_20201208_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersreal',
            name='dept_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depts', to='webapp.Department'),
        ),
        migrations.AlterField(
            model_name='usersreal',
            name='pic_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='webapp.Picture'),
        ),
        migrations.AlterField(
            model_name='usersreal',
            name='staff_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staffs', to='webapp.Staff'),
        ),
    ]
