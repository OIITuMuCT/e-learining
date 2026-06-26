from django.contrib.auth.models import User
from django.db import models


class Subject(models.Model):
    """ Модель предмета/дисциплины

    Представляет учебный предмет с уникальный URL-идентификатором (slug).

    Attributes:
        title (str): Название предмета. Обязательное поле
        slug (str): Уникальный URL-идентификатор. Генерируется автоматически
        из названия при сохранении, если не указан вручную.
    Example:
        >>> subject = Subject.objects.create(title="Programming")
        >>> subject.slug
        'programming'
    Note:
        Slug генерируется автоматически при первом сохранении.
    """
    title = models.CharField(max_length=200, verbose_name="Название",
                             help_text='Название предмета(например: "Математика", "Физика")')
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL-идентификатор",
                            help_text='Уникальный идентификатор для URL. Автоматически генерируется из названия.')

    class Meta:
        verbose_name ='Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['title']

    def __str__(self):
        """Возвращает строковое представление предмета"""
        return self.title


class Course(models.Model):
    """Модель Курса

    Представляет учебный курс определенного предмета
    Attributes:
        owner (User): преподаватель создавший курс
        subject (ForeignKey): предмет, к которому относится данный курс. Связанная модель: Subject
        title (str): Название курса
        slug (str): URL-идентификатор
        overview (str): Хранения краткий обзор курса.
        created (date): Дата и время создания курса.

    """
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        """Возвращает строковое представление курса"""
        return self.title


class Module(models.Model):
    """Модуль курса

    Представляет модули содержащиеся в определенном курсе
    Attributes:
        course (ForeignKey): Внешний ключ связан с моделью Course
        title (str): Название модуля
        description (str): Описание модуля
    """
    course = models.ForeignKey(
        Course, related_name='modules', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        """Возвращает строковое представление модуля"""
        return self.title

