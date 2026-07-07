from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.forms.models import modelform_factory
from django.apps import apps

from .models import Content, Course, Module
from .forms import ModuleFormSet



class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy("manage_course_list")

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    """Выводит список созданных пользователем крусов."""
    model = Course
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    """Использует модельную форму для создания объекта Course"""
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    """Класс обеспечивает возможность редактировать существующий объект Course"""
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    """Позволяет удалять Курс, через шаблон подтверждения удаления"""
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'

class CourseModuleUpdateView(TemplateResponseMixin, View):
    """CRUD

    Обрабатывает набор форм, служащий для добавления, обновления
    и удаления модулей определенного курса.
    TemplateResponseMixin: этот примесный класс отвечает за прорисовку шаблонов
    и возврат НТТР-ответа. Для него требуется атрибут template_name, указывающий
    на подлежащий прорисовке шаблон и предоставляющий метод render_to_response(),
    чтобы передавать ему контекст и прорисовывать шаблон.
    View: предоставляемое веб-фреймворком Django базовое представление на основе класса
    """
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        """Метод get_formset

        Определяется для избегания повторения исходного
        кода компоновки набора форм. Для заданного объекта Course,
        создается объект ModuleFormSet с опциональными данными
        """
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        """Метод класса View

        Принимает HTTP-запрос и его параметры
        """
        self.course = get_object_or_404(
            Course, id=pk, owner=request.user
        )
        return super().dispatch(request, pk)
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )
    def post(self , request, *args, **kwargs):
        """Метод выполняется для POST запросов.

        """
        # Создается экземпляр ModuleFormset
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response(
            {'course': self.course, 'formset': formset}
        )

class ContentCreateUpdateView(TemplateResponseMixin, View):
    """Модель позволяет создавать и обновлять содержимое разных моделей."""
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        """Проверяется принадлежность данного имени одной из четырех моделей
        содержимого: Text, Video, Image, File."""
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        """Создается динамическая форма, используя функцию modelform_factory() """
        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        """Получает следующие параметры праметры URL-адреса и сохраняет соответсвующий модуль,
        модель и объект содержимого в качестве атрибутов класса:
        module_id: ID модуля, с которым ассоциировано содержимое.
        model_name: Имя модели содержимого, которое нужно создать/обновить.
        id: ID обновляемого объекта. Он равен None, если создаются новые объекты.
        """
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, nodel_name, id=None):
        """Выполняется при получении запроса методом GET.

        Модельная форма компонуется для обновляемого экземпляра Text, Video, Image or File.
        В противном случае экземпляр для создания нового объекта не передается, поскольку,
        если ID не указан, то self.obj имеет значение None.
        """
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response(
            {'form': form, 'object': self.obj}
        )
    def post(self, request, module_id, model_name, id=None):
        """Выполняется при получении запроса методом POST.

        Модельная форма компонуется,
        передавая ей любые отправленные на обработку данные и файлы. Затем она валидируется.
        Если форма валидна, то создается новый объект, и request.user назначается его владельцем
        пред сохранением в БД.  Затем проверяется ID объекта, если он существует - создает новый объект,
        а не обновляет существующий.
        Для данного модуля создается объект Content и с ним связывается новое содержимое"""
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # новый контент
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})

class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(
            Content, id=id, module__course__owner=request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(
            Module, id=module_id, course__owner=request.user
        )
        return self.render_to_response({'module': module})
