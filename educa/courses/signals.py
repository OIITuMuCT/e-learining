from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

# Импортируем модели контента (укажите имя вашего приложения вместо .models, если нужно)
from .models import Content, Text, Video, File, Image

@receiver([post_save, post_delete], sender=Content)
@receiver([post_save, post_delete], sender=Text)
@receiver([post_save, post_delete], sender=Video)
@receiver([post_save, post_delete], sender=File)
@receiver([post_save, post_delete], sender=Image)
def clear_educational_platform_cache(sender, instance, **kwargs):
    """Гарантированно очищает кэш Redis при изменении любого типа контента"""
    cache.clear()
