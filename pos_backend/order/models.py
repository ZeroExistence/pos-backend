from django.db import models, transaction
from pos_backend.core.models import Item
from django.contrib.auth.models import User

# Create your models here.


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = (
        (1, "New"),
        (2, "Processing"),
        (3, "Completed"),
        (4, "Void")
    )

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=1
    )
    assigned = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    @property
    def total(self):
        total = 0
        for each in self.item.all():
            total += each.item_total
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='item',
        on_delete=models.CASCADE
    )
    name = models.ForeignKey(
        Item,
        on_delete=models.SET_NULL,
        null=True
    )
    quantity = models.PositiveIntegerField()
    current_price = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, editable=False
    )

    @property
    def item_total(self):
        if (self.current_price and self.quantity):
            return self.current_price * self.quantity
        else:
            return 0

    def save(self, *args, **kwargs):
        self.current_price = self.name.price
        super(OrderItem, self).save(*args, **kwargs)
