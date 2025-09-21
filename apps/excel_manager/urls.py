from django.urls import path
from . import views

app_name = "excel_manager"

urlpatterns = [
    # Main page with upload area and list
    path("", views.ExcelManagerView.as_view(), name="index"),
    # HTMX upload endpoint
    path("upload/", views.ExcelUploadView.as_view(), name="upload"),
    # Detail view for specific Excel file
    path("<int:pk>/", views.ExcelDetailView.as_view(), name="detail"),
    # HTMX partial for sheet switching
    path(
        "<int:pk>/sheet/<int:sheet_index>/",
        views.sheet_data_partial,
        name="sheet_data",
    ),
    # AI validation endpoint (HTMX)
    path(
        "<int:pk>/validate-ai/",
        views.ValidateWithAIView.as_view(),
        name="validate_ai",
    ),
    # Delete endpoint (HTMX)
    path(
        "<int:pk>/delete/",
        views.DeleteExcelView.as_view(),
        name="delete",
    ),
]
