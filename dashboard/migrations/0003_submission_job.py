# Generated by Django 3.2.3 on 2021-06-28 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='job',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.job'),
            preserve_default=False,
        ),
    ]
