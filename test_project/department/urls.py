from django.urls import path
from .views import TreeView


app_name = "department"

urlpatterns = [
    path('tree/', TreeView.as_view(), name='department-tree'),
]

