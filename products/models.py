from django.db import models
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        help_text="Rating must be between 1 and 5 (or other defined range)."
    )
    comment = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        unique_together = ("product", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review for {self.product.name} by {self.user} - {self.rating}/5"
