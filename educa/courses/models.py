from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .fields import OrderField

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
        verbose_name = 'Предмет'
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
        on_delete=models.CASCADE,
        verbose_name='Преподаватель'
    )
    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.CASCADE,
        verbose_name='Предмет'
    )
    title = models.CharField(max_length=200, verbose_name='Название',
                             help_text='Название курса(Например: Python, Django)')
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
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
    title = models.CharField(max_length=200, verbose_name='Модуль', help_text='Название модуля')
    description = models.TextField(blank=True, verbose_name='Краткое описание')
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        """Возвращает строковое представление модуля"""
        return f'{self.order}. {self.title}'


class Content(models.Model):
    """Модель Контент

    Устанавливает обобщенное отношение, чтобы связывать объекты из разных моделей,
    которые представляют разные типы содержимого.
    Attributes:
         content_type (ForeignKey): Связана с моделью: ContentType
         object_id (int): Поле для хранения первичного ключа связанного объекта
         item (GenericForeignKey): Поле для связанного объекта, объединяющее два предыдущих поля.
    Note: Text, File, Image, Video
    """
    module = models.ForeignKey(
        Module,
        related_name='contents',
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={'model__in':(
            'text',
            'video',
            'image',
            'file'
        )}
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    """Абстрактная модель

    Указанные поля будут использоваться для всех типов содержимого.
    Attributes:
        owner (str): хранит создавшего контент пользователя.
        title (str): Название контента
    """
    owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Text(ItemBase):
    """Модель Text для хранения тестового содержимого. """
    content = models.TextField()

class File(ItemBase):
    """Модель File для хранения файлов, например PDF-файлов."""
    file = models.FileField(upload_to=''
                                      'files')

class Image(ItemBase):
    """Модель Image для хранения файлов изображений."""
    file = models.ImageField(upload_to='images')

class Video(ItemBase):
    """Модель Video

    для хранения видео, поле URLField используется,
    чтобы предоставлять URL-адрес видео для его встраивания в контент.
    """
    url = models.URLField()

