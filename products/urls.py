from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ExportProductView, ProductViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = router.urls + [
    path("export/", ExportProductView.as_view(), name="export-products"),
]
