from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet
from .views import MovieListApiView
from django.views.decorators.cache import cache_page
router = DefaultRouter()
router.register(r'', MovieViewSet, basename='movies')

urlpatterns = [
    path('<str:version>/', MovieListApiView.as_view(), name='movie_list_api')
    # path('', views.MovieListApiView.as_view(), name='movie_list_api'),
    # path('<int:pk>/', views.MovieDetailApiView.as_view(), name='movie_detail_api'),

]

urlpatterns += router.urls
