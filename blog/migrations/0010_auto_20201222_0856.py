# Generated by Django 3.1.2 on 2020-12-22 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20201201_1520'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ratinganswers',
            options={'verbose_name': "Answers' rating", 'verbose_name_plural': "Answers' ratings"},
        ),
        migrations.AlterModelOptions(
            name='ratingquestions',
            options={'verbose_name': "Questions' rating", 'verbose_name_plural': "Questions' ratings"},
        ),
        migrations.AlterModelOptions(
            name='ratingusers',
            options={'verbose_name': "Users' rating", 'verbose_name_plural': "Users' ratings"},
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default.png', upload_to='avatar/%Y/%m/%d', verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='ratinganswers',
            name='to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.answer', verbose_name='Answer'),
        ),
        migrations.AlterField(
            model_name='ratinganswers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.profile', verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='ratingquestions',
            name='to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.question', verbose_name='Questions'),
        ),
        migrations.AlterField(
            model_name='ratingquestions',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.profile', verbose_name='Users'),
        ),
        migrations.AlterField(
            model_name='ratingusers',
            name='to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated_user', to='blog.profile', verbose_name='Rated user'),
        ),
    ]