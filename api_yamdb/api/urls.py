from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (AuthTokenView,
                    UserRegistrationView,
                    UserViewSet, CommentViewSet, ReviewViewSet,
                    CategoryViewSet, TitleViewSet, GenreViewSet
                    )

app_name = 'api'
router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('genres', GenreViewSet, basename='genres')

AUTH_URLPATTERNS = [
    path('auth/signup/',
         UserRegistrationView.as_view(),
         name='signup'),
    path('auth/token/',
         AuthTokenView.as_view(),
         name='auth'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(AUTH_URLPATTERNS))
]
