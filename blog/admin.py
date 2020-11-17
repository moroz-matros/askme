from django.contrib import admin
from blog import models

# Register your models here.

admin.site.register(models.Profile)

admin.site.register(models.Question)

admin.site.register(models.Tag)

admin.site.register(models.Answer)

admin.site.register(models.RatingUsers)
admin.site.register(models.RatingQuestions)
admin.site.register(models.RatingAnswers)

