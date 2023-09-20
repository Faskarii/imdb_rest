import json
from time import sleep

from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from django.shortcuts import render, redirect, get_object_or_404

from movies.models import Movie, MovieCrew
from movies.forms import MovieForm


@cache_page(5)
def movies_list(request):
    print('HERE')
    limit = int(request.GET.get('limit', 5))
    offset = int(request.GET.get('offset', 0))
    if request.method == 'GET':
        movies = Movie.objects.prefetch_related('genres')[offset:limit+offset]
        context = {
            "movies": movies,
            "is_valid": True
        }
        return render(request, 'movies/movies_list.html', context=context)

    elif request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('movies_list')

        return movie_add(request, form)


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk, is_valid=True)
    if request.method == 'GET':
        context = {
            'movie': movie,
            'movie_crew_list': MovieCrew.objects.filter(movie=movie).select_related('crew', 'role')
        }
        return render(request, 'movies/movie_detail.html', context=context)

    elif request.method == 'POST':
        # if login: request.user -> authenticated user
        # if not login: request -> AnonymousUser
        if request.user.is_authenticated:
            form = MovieForm(request.POST, request.FILES, instance=movie)
            if not form.is_valid():
                return movie_edit(request, pk, movie_form=form)

            form.save()
            return redirect('movie_detail', pk=pk)
        return redirect()


def movie_add(request, movie_form=None):
    if not movie_form:
        movie_form = MovieForm()
    return render(request, 'movies/movie_add.html', context={'form': movie_form})


def movie_edit(request, pk, movie_form=None):
    movie = get_object_or_404(Movie, pk=pk, is_valid=True)

    if not movie_form:
        movie_form = MovieForm(instance=movie)

    context = {
        'form': movie_form,
        'movie': movie
    }
    return render(request, 'movies/movie_edit.html', context=context)


def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk, is_valid=True)
    movie.is_valid = False
    movie.save()

    return redirect('movies_list')