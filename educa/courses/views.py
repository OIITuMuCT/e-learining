from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import Course
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