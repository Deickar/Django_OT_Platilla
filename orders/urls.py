from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.order_list, name="list"),
    path("nueva/", views.order_create, name="create"),
    path("<int:pk>/", views.order_detail, name="detail"),
    path("<int:pk>/editar/", views.order_edit, name="edit"),
    path("<int:pk>/eliminar/", views.order_delete, name="delete"),
    path("exportar/pdf/", views.export_pdf_list, name="export_pdf"),
    path("<int:pk>/pdf/weasy/", views.export_pdf_weasy, name="export_pdf_weasy"),
]
