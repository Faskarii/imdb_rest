import django_filters
from django_filters import FilterSet
from movies.models import Movie


class MovieFilterSet(FilterSet):
    min_release_date = django_filters.DateFilter(field_name='release_date', lookup_expr='gte')
    max_release_date = django_filters.DateFilter(field_name='release_date', lookup_expr='lt')


    class Meta:
        model = Movie
        fields = ('title', 'genres__title')