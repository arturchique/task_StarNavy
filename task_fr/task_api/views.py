from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


def index(request):
    return render(
        request,
        'index.html',
        locals()
    )


class PostView(APIView):
    """ Методы для работы с постом """

    def get(self, request):
        """ Возвращает информацию о заданном в параметре (?id=) посте """
        try:
            post_id = request.GET.get("id")
            if not post_id:
                raise ValueError
            post = Post.objects.get(id=post_id)
            return Response({
                "status": "ok",
                "data": {
                    "name": post.name,
                    "content": post.content,
                    "other_parameters": "Было б побольше параметров, использовал бы сериалайзер, но тут только текст(("
                }
            })
        except ValueError:
            return Response({
                "status": "error",
                "data": "Пропущен обязательный параетр GET запроса -- id поста (?id=<id поста>)"
            })
        except ObjectDoesNotExist:
            return Response({
                "status": "error",
                "data": "Поста с данными параметрами не существует"
            })

    def post(self, request):
        """ Метод для создания поста """
        if not request.user.is_authenticated:
            return Response({
                "status": "error",
                "data": "Используйте токен авторизованного пользователя, чтобы создать пост"
            })
        try:
            user = request.user
            content = request.data["content"]
            name = request.data["name"]
            new_post = Post(owner=user, content=content, name=name)
            new_post.save()
            return Response({
                "status": "ok",
                "data": f"Пост id={new_post.id} успешно сохранен"

            })
        except KeyError:
            return Response({
                "status": "error",
                "data": "Недостаточно данных для создания поста. Заполните обязательные поля: content, name"
            })


class PostsView(APIView):
    """ Методы для работы с массивами постов """

    def get(self, request):
        """ Возвращает данные обо всех постах пользователя заданного параметром (?user=)"""
        try:
            user_id = request.GET.get("user")
            if not user_id:
                raise ValueError
            user = USER.objects.get(id=user_id)
            posts = Post.objects.filter(owner=user)
            posts_serializer = PostSerializer(posts, many=True)
            return Response({
                "status": "ok",
                "data": {
                    "posts": posts_serializer.data,
                    "other": "Тут для приличия делаю с сериалайзером, все-таки я же знаю, что он есть и для чего он нужен"
                }
            })
        except ValueError:
            return Response({
                "status": "error",
                "data": "Недостает обязательных параметров (?user=<пользователь, чьи посты интересуют>)"
            })


class LikePostView(APIView):
    """ Лайкнуть пост с параметром ?id=<id поста> или убрать лайк"""

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({
                "status": "error",
                "data": "Отправьте запрос, указав токен аутентифицированного пользователя"
            })
        try:
            user = request.user
            post_id = request.data["id"]
            try:
                post = Post.objects.get(id=post_id)
            except ObjectDoesNotExist:
                # если передан несуществующий пост
                return Response({
                    "status": "error",
                    "data": "Такого поста не существует"
                })

            # Если лайк уже поставлен -- удаляем его
            like = Like.objects.get(liked_by=user, post=post)
            like.delete()
            return Response({
                "status": "ok",
                "data": "Лайк снят)))"
            })
        except ObjectDoesNotExist:
            like = Like(liked_by=user, post=post)
            like.save()
            # при добавлениии лайка -- убираем дизлайк
            try:
                dislike = Dislike.objects.get(disliked_by=user, post=post)
                dislike.delete()
            except ObjectDoesNotExist:
                pass

            return Response({
                "status": "ok",
                "data": "Пост лайкнут)))"
            })
        except KeyError:
            return Response({
                "status": "error",
                "data": "Недостает обязательных параметров ('id': <id понравившегося поста>)"
            })


class DislikePostView(APIView):
    """
    Дизлайкнуть пост с параметром ?id=<id поста> или убрать дизлайк
    Вообще, надо было бы по-умному написать, не повторяя кода,
    но задание на 3 часа, а мне сразу не пришла в голову гениальная мысль умного проектирования
    """

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({
                "status": "error",
                "data": "Отправьте запрос, указав токен аутентифицированного пользователя"
            })
        try:
            user = request.user
            post_id = request.data["id"]
            try:
                post = Post.objects.get(id=post_id)
            except ObjectDoesNotExist:
                # если передан несуществующий пост
                return Response({
                    "status": "error",
                    "data": "Такого поста не существует"
                })

            # Если лайк уже поставлен -- удаляем его
            dislike = Dislike.objects.get(disliked_by=user, post=post)
            dislike.delete()
            return Response({
                "status": "ok",
                "data": "Дизлайк снят)))"
            })
        except ObjectDoesNotExist:
            dislike = Dislike(disliked_by=user, post=post)
            dislike.save()
            # при добавлениии лайка -- убираем дизлайк
            try:
                like = Dislike.objects.get(liked_by=user, post=post)
                like.delete()
            except ObjectDoesNotExist:
                pass

            return Response({
                "status": "ok",
                "data": "Пост дизлайкнут)))"
            })
        except KeyError:
            return Response({
                "status": "error",
                "data": "Недостает обязательных параметров (?id=<id понравившегося поста>)"
            })


class LikesView(APIView):
    """ Возвращает количество лайков """

    def get(self, request):
        try:
            post_id = request.GET.get("id")
            if not post_id:
                raise ValueError
            date_from, date_to = request.GET.get('date_from'), request.GET.get('date_to')
            post = Post.objects.get(id=post_id)
            if not date_from and not date_to:
                likes = post.likes
            else:
                if not date_from:
                    likes = post.likes.filter(time__lte=date_to)
                elif not date_to:
                    likes = post.likes.filter(time__gte=date_from)
                else:
                    likes = post.likes.filter(time__range=(date_from, date_to))
            liked_users = []
            for like in likes.all():
                liked_users.append(like.liked_by)
            serializer = UserSerializer(liked_users, many=True)
            return Response({
                "status": "ok",
                "data": {
                    "liked_users": serializer.data
                }
            })

        except ValueError:
            return Response({
                "status": "error",
                "data": "Недостает обязательных параметров (?id=<id поста с лайками>)"
            })
        except ObjectDoesNotExist:
            return Response({
                    "status": "error",
                    "data": "Такого поста не существует"
                })


class DislikesView(APIView):
    """
    Возвращает количество дизлайков
    Включает возможность фильтрации дизлайков
    """

    # Мне, честно, очень стыдно за то, что я переписываю код для лайков второй раз, изменяя название переменной.
    def get(self, request):
        try:
            post_id = request.GET.get("id")
            if not post_id:
                raise ValueError
            date_from, date_to = request.GET.get('date_from'), request.GET.get('date_to')
            post = Post.objects.get(id=post_id)
            if not date_from and not date_to:
                dislikes = post.dislikes
            else:
                if not date_from:
                    dislikes = post.dislikes.filter(time__lte=date_to)
                elif not date_to:
                    dislikes = post.dislikes.filter(time__gte=date_from)
                else:
                    dislikes = post.dislikes.filter(time__range=(date_from, date_to))
            disliked_users = []
            for dislike in dislikes.all():
                disliked_users.append(dislike.disliked_by)
            serializer = UserSerializer(disliked_users, many=True)
            return Response({
                "status": "ok",
                "data": {
                    "disliked_users": serializer.data
                }
            })

        except ValueError:
            return Response({
                "status": "error",
                "data": "Недостает обязательных параметров (?id=<id поста с дизлайками>)"
            })
        except ObjectDoesNotExist:
            return Response({
                    "status": "error",
                    "data": "Такого поста не существует"
                })


class UserActivityView(APIView):
    """
    Возвращает информацию об активности пользователя,
    указанного в качестве гет параметра (?user_id=<айди пользователя>)
    """

    def get(self, request):
        user_id = request.GET.get("user_id")
        if not user_id:
            return Response({
                "status": "error",
                "data": "Недостает обязательных параметров (?user_id=<id пользователя>)"
            })
        user = USER.objects.get(id=user_id)
        serializer = UserActivitySerializer(user, many=False)
        return Response({
            "status": "ok",
            "data": serializer.data
        })