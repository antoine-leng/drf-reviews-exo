from rest_framework import viewsets, permissions, filters
from .models import Product
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer

@extend_schema(
    tags=["Products"],
    summary="CRUD Produits",
    description=(
        "Lister, créer, consulter, modifier et supprimer des produits.\n"
        "Supporte pagination (?page=) et tri (?ordering=price, -created_at, name)."
    ),
    request={
        "application/json": ProductSerializer,
        "application/xml": ProductSerializer,
    },
    responses={
        "application/json": ProductSerializer,
        "application/xml": ProductSerializer,
    },
    examples=[
        OpenApiExample(
            "Exemple de création",
            value={"name": "Pencil", "price": "1.99"},
            request_only=True,
            media_type="application/json",

        ),
        OpenApiExample(
            "Exemple de réponse",
            value={"id": 1, "name": "Pencil", "price": "1.99", "created_at": "2025-01-01T12:00:00Z"},
            response_only=True,
            media_type="application/json",
        ),
    ],
    parameters=[
        OpenApiParameter(
            name="ordering",
            description="Tri de la liste (ex: price, -created_at, name)",
            required=False,
            type=str,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="name",
            description="Filtrer par nom (égalité exacte)",
            required=False,
            type=str,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="price",
            description="Filtrer par prix (égalité exacte)",
            required=False,
            type=str,
            location=OpenApiParameter.QUERY,
        ),
    ],
)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, XMLParser]
    renderer_classes = [JSONRenderer, XMLRenderer]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["created_at", "price", "name"]
    ordering = ["-created_at"]
    filterset_fields = ["name", "price"]