import openpyxl
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from users.permissions import IsAdminOrReadOnly, IsAdminUser

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API for Product CRUD operations.
    - Users can only READ products.
    - Admins can CREATE, UPDATE, and DELETE products.
    """

    queryset = Product.objects.filter(is_active=True, is_deleted=False)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["title", "description", "price"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_on", "updated_on"]

    def perform_destroy(self, instance):
        """
        Soft delete: Instead of deleting, set `is_deleted=True`.
        """
        instance.soft_delete()
        return Response(
            {"message": "Product soft deleted successfully"},
            status=HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=['POST'], url_path='bulk-create/')
    def bulk_create(self, request):
        """
        Bulk Create Products
        """
        serializer = ProductSerializer(data=request.data, many=True)
        if serializer.is_valid():
            # Create all products in bulk
            products = Product.objects.bulk_create([Product(**data) for data in serializer.validated_data])
            return Response(
                {'message': f'{len(products)} products created successfully!'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=["POST"])
    def disable(self, request, pk=None):
        """
        Disable a product by setting `is_active=False`.
        """
        product = self.get_object()
        product.disable()
        return Response(
            {"message": "Product disabled successfully"}, status=HTTP_200_OK
        )

    @action(detail=True, methods=["POST"])
    def restore(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound({"error": "No Product matches the given query."})

        if product.is_deleted:
            raise ValidationError(
                {"error": "Product is permanently deleted and cannot be restored."}
            )

        if product.is_active:
            raise ValidationError({"error": "Product is already active."})

        product.is_active = True
        product.save()
        return Response(
            {"message": "Product restored successfully"}, status=HTTP_200_OK
        )


class ExportProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(is_active=True, is_deleted=False)
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["ID", "Title", "Description", "Price", "Discount"])

        for product in products:
            ws.append(
                [
                    product.id,
                    product.title,
                    product.description,
                    product.price,
                    product.discount,
                ]
            )

        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = 'attachment; filename="products.xlsx"'
        wb.save(response)
        return response
