from rest_framework import serializers
from movies.models import Movie, Genre, Crew, MovieCrew, Role
from rest_framework.exceptions import ValidationError
from django.utils import timezone


# class MovieSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     description = serializers.CharField()
#     release_date = serializers.DateField()
#     avatar = serializers.ImageField(required=False)
#     created_time = serializers.DateTimeField(read_only=True)
#
#     def create(self, validated_data):
#         # Movie.objects.create(
#         #     title=validated_data['title'],
#         #     description=validated_data['description'],
#         #     release_date=validated_data['release_data'],
#         #     avatar=validated_data.get['avatar']
#         # ) equals to below line
#
#         instance = Movie.objects.create(**validated_data)
#
#         return instance
#
#     def update(self, instance, validated_data):
#         pass


# MODEL SERIALIZER
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('title',)


class MovieCrewSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    crew = CrewSerializer()

    class Meta:
        model = MovieCrew
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200)
    temp_field = serializers.BooleanField(default=True)
    is_released = serializers.SerializerMethodField()
    genres = GenreSerializer(many=True)
    movie_crew = MovieCrewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'release_date',
                  'avatar', 'created_time',
                  'temp_field', 'is_released', 'genres', 'movie_crew')
        read_only_fields = ('created_time', )
        extra_kwargs = {'release_date': {'write_only': True}, 'avatar': {'required':False}}

    def get_is_released(self, obj):
        if not obj.release_date:
            return None

        return timezone.now().date() >= obj.release_date

    def create(self, validated_data):
        temp_field = validated_data.pop('temp_field')
        # instance = super(MovieSerializer, self).create(validated_data)
        # make for writable nested serializer

        genres = validated_data.pop('genres')
        instance = Movie.objects.create(**validated_data)
        for genre in genres:
            genre, created = Genre.objects.get_or_create(title=genre['title'])
            instance.genres.add(genre)

        if temp_field:
            pass
        return instance

    def update(self, instance, validated_data):
        pass

    def validate_title(self, attr):
         if 'ali' in attr:
            raise ValidationError('title should not contain ali')
         return attr.upper()

    def validate(self, attrs):
        release_date = attrs['release_date']
        avatar = attrs.get('avatar')
        date = timezone.datetime.strptime('2020-10-01', '%Y-%m-%d').date()
        if release_date > date and not avatar:
            raise ValidationError('This movie should have avatar')
        return attrs



