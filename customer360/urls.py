from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path(
        "communications/",
        views.communication_list,
        name="communication_list",
    ),

    path(
        "communications/add/",
        views.add_communication,
        name="add_communication",
    ),

    path(
        "communications/<int:pk>/",
        views.customer_detail,
        name="customer_detail",
    ),

    path(
        "communications/<int:pk>/edit/",
        views.edit_communication,
        name="edit_communication",
    ),

    path(
        "communications/<int:pk>/delete/",
        views.delete_communication,
        name="delete_communication",
    ),

    path(
        "communications/export/",
        views.export_csv,
        name="export_csv",
    ),
]