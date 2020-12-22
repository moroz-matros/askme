from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from django.db.models.signals import post_save
from django.dispatch import receiver

class ProfileManager(models.Manager):
    def find_id(self, profile_id):
        return self.get(id=profile_id)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    email = models.EmailField(max_length=256, verbose_name = "Email", default="")
    nickname = models.CharField(max_length=256, verbose_name='Nickname')
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', verbose_name="Avatar", 
        default="default.png")
    reg_date = models.DateField(verbose_name="Registration date", default=date.today)
    rate = models.IntegerField(default=0, verbose_name="Rate")
    objects = ProfileManager()

    def __str__(self):
        return self.nickname


    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class QuestionManager(models.Manager):
    def find_id(self, question_id):
        return self.get(id=question_id)

    def find_tag(self, tag):
        return self.filter(tags__word__icontains=tag)


class Question(models.Model):
    title = models.CharField(max_length=1024, verbose_name='Title')
    text = models.TextField(verbose_name='Text', default="")
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    creation_date = models.DateField(verbose_name="Creation date",default=date.today)
    tags = models.ManyToManyField("Tag", verbose_name="Tags")
    rate = models.IntegerField(default=0, verbose_name="Rate")
    objects = QuestionManager()

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.title

class TagManager(models.Manager):
    def find_id(self, tag_id):
        return self.get(id=tag_id)


class Tag(models.Model):
    word = models.CharField(max_length=256, verbose_name="Tag")
    objects = TagManager()

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class AnswerManager(models.Manager):
    def find_id(self, answer_id):
        return self.get(id=answer_id)

    def count(self, question_id):
        return self.filter(question = question_id).count()

    def find_by_q(self, question_id):
        return self.filter(question = question_id)


class Answer(models.Model):
    text = models.TextField(verbose_name='Text', default="")
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    creation_date = models.DateField(verbose_name="Creation date",default=date.today)
    flag = models.BinaryField(verbose_name="Correct answer?", default=0)
    rate = models.IntegerField(default=0, verbose_name="Rate")
    objects = AnswerManager()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

class RatingManagerQuestions(models.Manager):
    def find_id(self, id):
        return self.get(id=id)

    def find_eu(self, element, user):
        return self.filter(to=element).filter(user=user)

    def change_rate(self, qid, user, action):
        question = Question.objects.find_id(qid)
        rate = RatingQuestions.objects.create(user=user, to=question)
        rate.save()
        if action == "like":
            question.rate += 1
        else:
            question.rate -= 1
        question.save()
        return question.rate

class RatingUsers(models.Model):
    user = models.ForeignKey('Profile', related_name="user_profile", on_delete=models.CASCADE, 
        verbose_name="User")
    to = models.ForeignKey('Profile', related_name="rated_user",on_delete=models.CASCADE, 
        verbose_name="Rated user")
    #objects = RatingManager()

    class Meta:
        verbose_name = "Users' rating"
        verbose_name_plural = "Users' ratings"

class RatingQuestions(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, 
        verbose_name="Users")
    to = models.ForeignKey('Question', on_delete=models.CASCADE, 
        verbose_name="Questions")
    objects = RatingManagerQuestions()

    def __str__(self):
        return "rate"

    class Meta:
        verbose_name = "Questions' rating"
        verbose_name_plural = "Questions' ratings"

class RatingAnswers(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, 
        verbose_name="User")
    to = models.ForeignKey('Answer', on_delete=models.CASCADE, 
        verbose_name="Answer")
    #objects = RatingManager()

    class Meta:
        verbose_name = "Answers' rating"
        verbose_name_plural = "Answers' ratings"