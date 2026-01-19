# Тестовое задание для ТЛ групп
<img width="3154" height="1642" alt="image_test" src="https://github.com/user-attachments/assets/0fc5bec5-f6b5-42b4-b9ea-85d44553d956" />

## Запуск
1)спулить репозиторию  
2)создать в корне .env файл и добавить туда переменные окружения  
например:
```
DJANGO_SECRET_KEY=django-insecure-9d3aee3b2e6241d0b9cfb72f8e0986af3d7c1d2c14e5a72f8b
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=test_db
POSTGRES_USER=test_user
POSTGRES_PASSWORD=test_password
POSTGRES_HOST=postgres_test
POSTGRES_PORT=5432

# Legacy variable names (if referenced elsewhere)
DB_NAME=test_db
DB_USER=test_user
DB_PASSWORD=test_password
```
3) ```docker compose up --build / docker-compose up -build```  
4) можно запустить скрипт генерации тестовых данных  
4.1) ```docker exec -it {id контейнера} bash```   
4.2) ```python manage.py generate_test_data```  
4) ```http://127.0.0.1:8000/department/tree/```  

Суть задания: бэк и фронт (шаблон с bootstrap) древовидной структуры отделов и списка сотрудников.


Стек: Python3.12, Django6.0.1, Postgres, Bootstrap5.

Используется библиотека https://github.com/feincms/django-tree-queries для создания древовидной структуры отделов

```
#models.py
from django.db import models
from tree_queries.models import TreeNode <-----

class Department(TreeNode): <-------
    name = models.CharField(max_length=255, unique=True, verbose_name='Название департамента')

    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"
    
    def __str__(self):
        return self.name

    def get_full_path(self):
        return " → ".join(anc.name for anc in self.ancestors(include_self=True))
```
# Подход к решению задачи
Cразу префетчим сотрудников, чтобы в шаблоне не было N+1 запросов.
```
views.py
from django.views.generic import TemplateView

from .models import Department, Employee

class TreeView(TemplateView):
    template_name = 'department/tree.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments_qs = (
            Department.objects.with_tree_fields() <----
            .prefetch_related("employees") <-------
        )

        context.update(
            {
                "departments": departments_qs,
            }
        )


        return context

```
## Нынешний подход
-Загружаем всё дерево + всех сотрудников.

-Оптимизируем ORM (prefetch).

-Плюсы: простая реализация, один prefetch-запрос, нет N+1.

-Минусы: большой объём HTML, много памяти (Django и браузер).



### Вариант оптимизации при росте до сотен тысяч / миллионов Сотрудников.
На стартовой странице рендерим только дерево отделов.

При клике на отдел:
JS делает запрос /department/<id>/employees/,
backend возвращает сотрудников этого отдела (можно пагинировать),
фронт динамически вставляет список.
