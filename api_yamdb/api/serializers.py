from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import (Category, Genre, Title,
                            Comment, Review, User)
from reviews.validators import check_year, validate_username


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def validate_year(self, value):
        return check_year(value)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    score = serializers.IntegerField(validators=(
        MinValueValidator(1, 'Минимальная оценка 1'),
        MaxValueValidator(10, 'Максимальная оценка 10')
    ))

    class Meta:
        exclude = ('title', )
        model = Review

    def validate(self, data):
        if self.context.get('request').method == 'PATCH':
            return data
        if get_object_or_404(
            Title,
            id=self.context['view'].kwargs.get('title_id')
        ).reviews.filter(author=self.context.get('request').user).exists():
            raise serializers.ValidationError(
                'Нельзя оставить более одного отзыва.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        exclude = ('review', )
        model = Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        return validate_username(value)


class TitleViewSerializer(serializers.ModelSerializer):
    """Основной метод получения информации."""
    category = CategorySerializer(many=False, required=True)
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = Title


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=settings.USERNAME_MAX_LEN
    )
    email = serializers.EmailField(
        required=True,
        max_length=settings.EMAIL_MAX_LEN
    )

    def validate_username(self, value):
        return validate_username(value)


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=settings.USERNAME_MAX_LEN)
    confirmation_code = serializers.CharField(
        max_length=settings.CODE_LEN, required=True
    )

    def validate_username(self, value):
        return validate_username(value)
