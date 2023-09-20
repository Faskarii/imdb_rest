from django.contrib import admin
from .models import Movie, Role, Crew, Genre, MovieCrew


class RoleAdmin(admin.ModelAdmin):
    list_display = ('title',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class MCInline(admin.TabularInline):
    model = MovieCrew
    extra = 1


class GenreInline(admin.StackedInline):
    model = Movie.genres.through
    extra = 1


class CrewAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    inlines = [MCInline]


class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'release_date']
    search_fields = ['title']
    inlines = [MCInline, GenreInline]
    exclude = ('genres',)


admin.site.register(Role, RoleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Crew, CrewAdmin)