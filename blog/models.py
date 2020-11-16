from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя')
    birthday = models.DateField(verbose_name='Дата рождения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class QuestionManager(models.Manager):
    def find_id(self, question_id):
        return self.get(id=question_id)

class Question(models.Model):
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст', default="")
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    tags = models.CharField(max_length=1024, verbose_name='Теги')
    objects = QuestionManager()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
