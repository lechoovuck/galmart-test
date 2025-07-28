from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response


@extend_schema_view(
    list=extend_schema(
        summary="List all products",
        description="Retrieve a list of all products."
    ),
    retrieve=extend_schema(
        summary="Retrieve a product",
        description="Get details of a specific product by its ID."
    ),
    create=extend_schema(
        summary="Create a product",
        description="Add a new product to the catalog."
    ),
    update=extend_schema(
        summary="Update a product",
        description="Update the details of an existing product."
    ),
    partial_update=extend_schema(
        summary="Partially update a product",
        description="Update some fields of an existing product."
    ),
    destroy=extend_schema(
        summary="Delete a product",
        description="Remove a product from the catalog."
    ),
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)
