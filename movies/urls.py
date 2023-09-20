from django.urls import path, include
from django.views.decorators.cache import cache_page
from . import views
urlpatterns =[
    path('', views.movies_list, name='movies_list'),
    path('detail/<int:id>', views.movie_detail, name='movie_detail'),
    path('api/', include('movies.api.urls')),

]