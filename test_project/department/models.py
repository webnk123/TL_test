from django.db import models
from django.utils import timezone
from tree_queries.models import TreeNode
from django.utils.translation import gettext_lazy as _
# https://github.com/feincms/django-tree-queries


class Department(TreeNode):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название департамента')

    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"

    def __str__(self):
        return self.name

    def get_full_path(self):
        return " → ".join(
            anc.name for anc in self.ancestors(
                include_self=True))


class Employee(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    patronymic = models.CharField(max_length=150, blank=True, null=False)
    position = models.CharField(max_length=200)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=12, decimal_places=2)

    department = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        verbose_name=_("Подразделение"),
        related_name="employees",
    )

    class Meta:
        verbose_name = _("Сотрудник")
        verbose_name_plural = _("Сотрудники")

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        parts = [self.last_name.strip()]

        if self.first_name.strip():
            parts.append(self.first_name.strip())

        if self.patronymic.strip():
            parts.append(self.patronymic.strip())

        return " ".join(parts)
