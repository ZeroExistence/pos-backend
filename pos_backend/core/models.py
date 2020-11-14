from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class VariantType(models.Model):
    type = models.CharField(max_length=100, unique=True)
    weight = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ["weight", "type"]


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    sku = models.CharField(max_length=100, blank=True, null=True)

    def get_variant(self):
        return ', '.join([variant.type for variant in self.variant.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.product.name, ', '.join([variant.type for variant in self.variant.all()]))


class Variant(models.Model):
    item = models.ForeignKey(
        Item,
        related_name='variant',
        on_delete=models.CASCADE
    )
    name = models.ForeignKey(
        VariantType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type
