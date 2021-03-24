from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()


class Post(models.Model):
    owner = models.ForeignKey(USER, on_delete=models.CASCADE, verbose_name="Владелец поста",
                              help_text="Владелец поста", related_name="posts")
    name = models.CharField(max_length=100, help_text="Название", verbose_name="Название")
    content = models.TextField(max_length=300, help_text="Контент", verbose_name="Контент")


""" 
Делаю лайки и дизлайки разными моделями, чтобы было возможно далее
прикрутить аналитику, для которой будем возвращать
лайки и дизлайки отдельно, обращаясь к ним через разные related_name

Логичнее было бы пронаследоваться от асбтрактного класса и изменить только 
related_name у полей, но я этого делать ну буду, потому что у классов всего по три поля
"""


class Like(models.Model):
    liked_by = models.ForeignKey(USER, on_delete=models.CASCADE, verbose_name="Пользователь",
                                 help_text="Пользователь", related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes',
                             help_text="Пост", verbose_name="Пост")
    time = models.DateTimeField(auto_now=True, verbose_name="Время лайка", help_text="Время лайка")


class Dislike(models.Model):
    disliked_by = models.ForeignKey(USER, on_delete=models.CASCADE, verbose_name="Пользователь",
                                    help_text="Пользователь", related_name="dislikes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='dislikes',
                             help_text="Пост", verbose_name="Пост")
    time = models.DateTimeField(auto_now=True, verbose_name="Время дизлайка", help_text="Время дизлайка")

