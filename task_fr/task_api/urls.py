from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from .views import *


schema_view = get_schema_view(
   openapi.Info(
      title="S2B API",
      default_version='v1',
      description="Описание",
      terms_of_service="https://github.com/arturchique/s2b",
      contact=openapi.Contact(email="aepremyan3993@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('post/', PostView.as_view()),
    path('posts/', PostsView.as_view()),
    path('post/likes/', LikesView.as_view()),
    path('post/dislikes/', DislikesView.as_view()),
    path('post/like/', LikePostView.as_view()),
    path('post/dislike/', DislikePostView.as_view()),
    path('user/activity/', UserActivityView.as_view()),
    path('', index),

]