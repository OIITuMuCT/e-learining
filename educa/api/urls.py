from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
@permission_classes([AllowAny])
@extend_schema(exclude=True)
def api_root(request, format=None):
    """Единая точка входа для всего API"""
    return Response({
        'courses': reverse('api:courses_api:course-list', request=request, format=format),
        'subjects': reverse('api:courses_api:subject-list', request=request, format=format),

        # Ссылка на пример эндпоинта записи на курс (передаем pk=1 как пример структуры URL)
        'course_enroll_example': reverse('api:courses_api:course_enroll', kwargs={'pk': 1}, request=request, format=format),

        # Ссылки из приложения студентов (пространство имен 'students_api')
        'student_registration': reverse('api:students_api:student_registration', request=request, format=format),
        'student_login': reverse('api:students_api:token_obtain_pair', request=request, format=format),
        'student_token_refresh': reverse('api:students_api:token_refresh', request=request, format=format),

    })

apps_urlpatterns = [
    path('students/', include('students.api.urls')),
    path('', include('courses.api.urls')),

]

app_name = 'api'

urlpatterns = [
    path('', api_root, name='root'),
    path('', include(apps_urlpatterns)),
]