from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from rest_framework.versioning import URLPathVersioning
from rest_framework.views import APIView
from rest_framework import mixins, generics

from .filters import MovieFilterSet
from .serializers import MovieSerializer
from movies.models import Movie
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.authentication import JWTAuthentication
from movies.throttles import MovieListThrottle

@api_view(['GET', 'POST'])
def movie_list_api(request):
    if request.method == 'GET':
        movies = Movie.objects.prefetch_related('genres', 'crew')
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
         serializer = MovieSerializer(data=request.data, status=status.HTTP_201_CREATED)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response(serializer.data)


class MovieListApiView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.prefetch_related('genres', 'crew')
    versioning_class = URLPathVersioning
    #
    def get(self, request, *args, **kwargs):
        print('version', request.version)
        return self.list(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     print('version', request.version)

class MovieDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.prefetch_related('genres', 'crew')


class MovieViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Movie.objects.prefetch_related('genres', 'crew')
    serializer_class = MovieSerializer
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'movies'
    # pagination_class = LimitOffsetPagination
    filter_backends = [ SearchFilter, DjangoFilterBackend]
    # filterset_fields = ('genres', )
    search_fields = ('title',)
    filterset_class = MovieFilterSet
    def get_throttles(self):
        if self.action == 'list':
            return [MovieListThrottle()]

        return [ScopedRateThrottle]

    def list(self, request, *args, **kwargs):
        print(request.user)
        return super(MovieViewSet, self).list(request, *args, **kwargs)

    def get_permissions(self):
         if self.action == "list":
            return [IsAuthenticatedOrReadOnly()]

    # def create(self, request, *args, **kwargs):
    #     return Response()
    #
    # def update(self, request, *args, **kwargs):
    #     return Response()
    #
    # def partial_update(self, request, *args, **kwargs):
    #     return Response()
    #
    # def destroy(self, request, *args, **kwargs):
    #     return Response()