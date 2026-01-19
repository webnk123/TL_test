# department/management/commands/generate_data.py

from django.core.management.base import BaseCommand
import random
from department.models import Department, Employee


class Command(BaseCommand):
    help = 'Создаёт простое дерево отделов и 50 000 сотрудников'

    def handle(self, *args, **options):
        # 1. Создаём ~25 отделов в 5 уровнях
        departments = []

        # 5 корневых
        for i in range(5):
            dept = Department.objects.create(name=f"Отдел {i+1}")
            departments.append(dept)

        # Добавляем детей (примерно до 25 всего)
        parents = departments[:]
        while len(departments) < 25:
            new_parents = []
            for p in parents:
                if len(departments) >= 25:
                    break
                for _ in range(random.randint(0, 2)):
                    if len(departments) >= 25:
                        break
                    child = Department.objects.create(
                        parent=p,
                        name=f"{p.name} → Подотдел {len(departments)+1}"
                    )
                    departments.append(child)
                    new_parents.append(child)
            parents = new_parents or parents  # если не добавили — не зацикливаемся

        self.stdout.write(f"Создано отделов: {len(departments)}")

        # 2. Создаём 50 000 сотрудников
        employees = []
        positions = ["Менеджер", "Специалист", "Инженер", "Аналитик", "Разработчик"]

        for i in range(50000):
            emp = Employee(
                first_name=f"Имя{i+1}",
                last_name=f"Фамилия{i+1}",
                patronymic="",
                position=random.choice(positions),
                hire_date="2020-01-01",  # фиксированная дата для простоты
                salary=random.randint(80000, 250000),
                department=random.choice(departments)
            )
            employees.append(emp)

        Employee.objects.bulk_create(employees, batch_size=5000)

        self.stdout.write(self.style.SUCCESS(
            f"Готово. Сотрудников: {Employee.objects.count()}"
        ))