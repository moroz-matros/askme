# Generated by Django 3.1.2 on 2020-11-28 15:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_auto_20201117_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='uploads/default.png', upload_to='uploads/', verbose_name='Аватар'),
        ),
    ]
