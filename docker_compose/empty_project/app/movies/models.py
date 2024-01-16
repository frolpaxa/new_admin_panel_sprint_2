import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Roles(models.TextChoices):
    ACTOR = "actor", _("actor")
    DIRECTOR = "director", _("Director")
    WRITER = "writer", _("Writer")


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")

    def __str__(self):
        return self.name


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    genre = models.ForeignKey(
        "Genre", on_delete=models.CASCADE, verbose_name=_("genre")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")
        indexes = [
            models.Index(fields=["film_work", "genre"]),
            models.Index(fields=["film_work"], name="film_work_genre_idx"),
        ]

    def __str__(self):
        return ""


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full name"), max_length=255)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("actor")
        verbose_name_plural = _("actors")

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, verbose_name=_("person")
    )
    role = models.TextField(
        _("Role"),
        null=True,
        choices=Roles.choices,
        default=Roles.ACTOR,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _("actor")
        verbose_name_plural = _("actors")
        indexes = [
            models.Index(fields=["film_work", "person"]),
            models.Index(fields=["film_work"], name="film_work_person_idx"),
        ]

    def __str__(self):
        return ""


class FilmworkType(models.TextChoices):
    MOVIE = "movie", _("Movie")
    BAT = "tv_show", _("TV Show")


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("title"), blank=True, null=True)
    creation_date = models.DateTimeField(
        _("creation date"), auto_now_add=True, null=True
    )
    rating = models.FloatField(
        _("rating"),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
    )
    type = models.CharField(
        _("type"),
        max_length=7,
        choices=FilmworkType.choices,
        default=FilmworkType.MOVIE,
    )
    genres = models.ManyToManyField(Genre, through="GenreFilmwork")
    persons = models.ManyToManyField(Person, through="PersonFilmwork")
    file_path = models.CharField(_("File path"), max_length=250, blank=True, null=True)

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("work")
        verbose_name_plural = _("works")

    def __str__(self):
        return self.title
