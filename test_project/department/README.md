#Тестовое задание для ТЛ групп#

Суть задания: бэк и фронт (шаблон с bootstrap) древовидной структуры отделов и списка сотрудников.


Стек: Python3.12, Django6.0.1, Postgres, Bootstrap5
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
##Подход к решению задачи ##

Cразу префетчим сотрудников, чтобы в шаблоне не было N+1 запросов.
```
#views.py
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
## Нынешний подход ##
-Загружаем всё дерево + всех сотрудников.
-Оптимизируем ORM (prefetch).
Плюсы: простая реализация, один prefetch-запрос, нет N+1.
Минусы: большой объём HTML, много памяти (Django и браузер).


##Вариант оптимизации при росте до сотен тысяч / миллионов Сотрудников. ##
На стартовой странице рендерим только дерево отделов.
При клике на отдел:
JS делает запрос /department/<id>/employees/,
backend возвращает сотрудников этого отдела (можно пагинировать),
фронт динамически вставляет список.
