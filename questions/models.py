from django.db import models
from django.conf import settings


class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=240)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="questions")

    up_voters = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name="qupvotes")
    down_voters = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name="qdownvotes")

    def __str__(self):
        return self.content


class Answer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField()
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name="answers")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    up_voters = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name="aupvotes")
    down_voters = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name="adownvotes")

    def __str__(self):
        return str(self.question.id) + "-" + self.author.username


class Tag(models.Model):
    tag_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.tag_name
