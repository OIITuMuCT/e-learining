# api/spectacular_hooks.py

def custom_preprocessing_hook(endpoints):
    """
    Автоматически группирует эндпоинты по тегам на основе структуры URL
    """
    filtered_endpoints = []

    for path, path_regex, method, callback in endpoints:
        # Исключаем технический корень API из документации
        if path == '/api/v1/':
            continue

        # Получаем объект View
        view = callback.cls if hasattr(callback, 'cls') else None

        if view:
            # Способ 1: Проверяем по URL-пути
            if '/students/' in path:
                view.initkwargs['tags'] = ['Students']
            elif '/courses/' in path or path.startswith('/api/v1/courses'):
                view.initkwargs['tags'] = ['Courses']

            # Способ 2 (Альтернативный): Можно проверять по названию модуля класса
            # module_name = view.__module__
            # if 'students' in module_name:
            #     view.initkwargs['tags'] = ['Students']

        filtered_endpoints.append((path, path_regex, method, callback))

    return filtered_endpoints

