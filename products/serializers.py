from rest_framework import serializers
from .models import Product, Review


class ProductSerializer(serializers.ModelSerializer):
    """
    Représentation d'un produit vendable. (Representation of a sellable product.)
    - name: nom commercial (commercial name)
    - price: prix TTC en euros (price including tax, must be > 0)
    - created_at: horodatage de création (creation timestamp, read-only)
    """

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("created_at",)

    def validate_price(self, value):
        """Ensures the price is positive."""
        if value <= 0:
            raise serializers.ValidationError("Le prix doit être > 0")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the Review model."""

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("user", "created_at")

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La note doit être entre 1 et 5.")
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        if request and request.method == "POST":
            product = attrs.get("product")
            if (
                product
                and Review.objects.filter(product=product, user=request.user).exists()
            ):
                raise serializers.ValidationError(
                    "Vous avez déjà laissé un avis pour ce produit."
                )
        return attrs
