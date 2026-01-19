from django.views.generic import TemplateView

from .models import Department, Employee


class TreeView(TemplateView):
    template_name = 'department/tree.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments_qs = (
            Department.objects.with_tree_fields()
            .prefetch_related("employees")
        )

        context.update(
            {
                "departments": departments_qs,
            }
        )

        return context
