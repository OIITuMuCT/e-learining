from django.forms.models import inlineformset_factory

from .models import Course, Module
"""
Inlineformset_factory

    fields:  поля, которые будут включены в каждую форму набора форм.
    extra: позволяет устанавливать число пустых дополнительных форм для отображения в наборе форм.
    can_delete: если значение этого параметра устанавливается True, то Django 
    будет вставлять булево поле для каждой формы, которая будет прорисовываться в виде флажка. 
    Этим обеспечивается возможность помечать объекты, которые требуется удалить.
"""
ModuleFormSet = inlineformset_factory(Course, Module, fields=['title', 'description'], extra=2, can_delete=True)
