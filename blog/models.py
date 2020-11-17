from django.db import models
from django.utils import timezone
from datetime import date

class ProfileManager(models.Manager):
    def find_id(self, profile_id):
        return self.get(id=profile_id)


class Profile(models.Model):
    email = models.EmailField(max_length=256, verbose_name = "Email", default="")
    nickname = models.CharField(max_length=256, verbose_name='Никнейм')
    avatar = models.ImageField(upload_to='uploads/', verbose_name="Аватар", blank=True, 
        default="uploads/default.png")
    reg_date = models.DateField(verbose_name="Дата регистрации", default=date.today)
    rate = models.IntegerField(default=0, verbose_name="Рейтинг")
    objects = ProfileManager()

    def __str__(self):
        return self.nickname


    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class QuestionManager(models.Manager):
    def find_id(self, question_id):
        return self.get(id=question_id)

    def find_tag(self, tag):
        return self.filter(tags__word__icontains=tag)


class Question(models.Model):
    title = models.CharField(max_length=1024, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст', default="")
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    creation_date = models.DateField(verbose_name="Дата создания",default=date.today)
    tags = models.ManyToManyField("Tag", verbose_name="Теги")
    rate = models.IntegerField(default=0, verbose_name="Рейтинг")
    objects = QuestionManager()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.title

class TagManager(models.Manager):
    def find_id(self, tag_id):
        return self.get(id=tag_id)


class Tag(models.Model):
    word = models.CharField(max_length=256, verbose_name="Тег")
    objects = TagManager()

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class AnswerManager(models.Manager):
    def find_id(self, answer_id):
        return self.get(id=answer_id)

    def count(self, question_id):
        return self.filter(question = question_id).count()

    def find_by_q(self, question_id):
        return self.filter(question = question_id)


class Answer(models.Model):
    text = models.TextField(verbose_name='Текст', default="")
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    creation_date = models.DateField(verbose_name="Дата написания",default=date.today)
    flag = models.BinaryField(verbose_name="Верный ответ?", default=0)
    rate = models.IntegerField(default=0, verbose_name="Рейтинг")
    objects = AnswerManager()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

class RatingManager(models.Manager):
    def find_id(self, id):
        return self.get(id=id)

class RatingUsers(models.Model):
    user = models.ForeignKey('Profile', related_name="user_profile", on_delete=models.CASCADE, 
        verbose_name="Пользователь")
    to = models.ForeignKey('Profile', related_name="rated_user",on_delete=models.CASCADE, 
        verbose_name="Оцененный пользователь")
    objects = RatingManager()

    class Meta:
        verbose_name = 'Рейтинг пользователей'
        verbose_name_plural = 'Рейтинги пользователей'

class RatingQuestions(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, 
        verbose_name="Пользователь")
    to = models.ForeignKey('Question', on_delete=models.CASCADE, 
        verbose_name="Вопрос")
    objects = RatingManager()

    class Meta:
        verbose_name = 'Рейтинг вопросов'
        verbose_name_plural = 'Рейтинги вопросов'

class RatingAnswers(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, 
        verbose_name="Пользователь")
    to = models.ForeignKey('Answer', on_delete=models.CASCADE, 
        verbose_name="Ответ")
    objects = RatingManager()

    class Meta:
        verbose_name = 'Рейтинг ответов'
        verbose_name_plural = 'Рейтинги ответов'