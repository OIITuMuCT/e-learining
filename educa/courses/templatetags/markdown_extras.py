import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
@stringfilter
def convert_markdown(value):
    # Настраиваем расширения, добавляя codehilite
    extensions = [
        "markdown.extensions.fenced_code",  # Поддержка блоков ```bash
        "markdown.extensions.tables",       # Поддержка таблиц
        "markdown.extensions.codehilite",   # Подсветка синтаксиса
        "markdown_checklist.extension",     # Добавил чекбоксы
        "markdown.extensions.admonition",   # Для синтаксиса !!! note
        "gfm_admonition",                # Для синтаксиса [!NOTE]
    ]

    extensions_configs = {
        "markdown.extensions.codehilite": {
            "css_class": "highlight",
            "guess_lang": False,
        }
    }

    html = markdown.markdown(
        value,
        extensions=extensions,
        extension_configs=extensions_configs
    )

    # mark_safe сообщает Django, что это HTML проверен и его можно рендерить
    return mark_safe(html)