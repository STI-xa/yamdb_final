from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import check_year, validate_username


class CategoryGenreGeneralModel(models.Model):

    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name[:30]


class Category(CategoryGenreGeneralModel):
    """Типы произведений"""

    class Meta(CategoryGenreGeneralModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreGeneralModel):
    """Жанры произведений"""

    class Meta(CategoryGenreGeneralModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведения"""
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование произведения'
    )
    year = models.IntegerField(
        verbose_name='Год произведения',
        validators=[check_year],
        null=True

    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self) -> str:
        return self.name[:30]


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=settings.USERNAME_MAX_LEN,
        unique=True,
        validators=[validate_username]
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        'Роль',
        max_length=max(len(role) for role, _ in USER_ROLES),
        default=USER,
        choices=USER_ROLES
    )
    email = models.EmailField(
        'Почта',
        unique=True,
        max_length=settings.EMAIL_MAX_LEN
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=settings.CODE_LEN,
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user'),
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class GeneralFieldsCommentReview(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='%(class)ss',
    )
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Review(GeneralFieldsCommentReview):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(1, 'Минимальная оценка 1'),
            MaxValueValidator(10, 'Максимальная оценка 10')
        )
    )

    class Meta(GeneralFieldsCommentReview.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_title_author'
            ),
        )


class Comment(GeneralFieldsCommentReview):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')

    class Meta(GeneralFieldsCommentReview.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
