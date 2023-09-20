from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from movies.models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'description', 'release_date', 'avatar',)