# Generated by Django 3.1.2 on 2020-11-16 22:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='', verbose_name='Текст')),
                ('creation_date', models.DateField(default=datetime.date.today, verbose_name='Дата написания')),
                ('flag', models.BinaryField(default=0, verbose_name='Верный ответ?')),
                ('rate', models.IntegerField(default=0, verbose_name='Рейтинг')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='', max_length=256, verbose_name='Email')),
                ('nickname', models.CharField(max_length=256, verbose_name='Никнейм')),
                ('avatar', models.ImageField(default='', height_field=128, upload_to='uploads/', verbose_name='Аватар', width_field=128)),
                ('reg_date', models.DateField(default=datetime.date.today, verbose_name='Дата регистрации')),
                ('rate', models.IntegerField(default=0, verbose_name='Рейтинг')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='Заголовок')),
                ('text', models.TextField(default='', verbose_name='Текст')),
                ('creation_date', models.DateField(default=datetime.date.today, verbose_name='Дата создания')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.profile')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=256, verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='RatingUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated_user', to='blog.profile', verbose_name='Оцененный пользователь')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to='blog.profile', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Рейтинг пользователей',
                'verbose_name_plural': 'Рейтинги пользователей',
            },
        ),
        migrations.CreateModel(
            name='RatingQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.question', verbose_name='Вопрос')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.profile', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Рейтинг вопросов',
                'verbose_name_plural': 'Рейтинги вопросов',
            },
        ),
        migrations.CreateModel(
            name='RatingAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.answer', verbose_name='Ответ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.profile', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Рейтинг ответов',
                'verbose_name_plural': 'Рейтинги ответов',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.profile'),
        ),
    ]
