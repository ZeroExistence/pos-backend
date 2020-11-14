from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem
from pos_backend.core.models import Item


class OrderSerializer(serializers.ModelSerializer):
    class TempOrderItemSerializer(serializers.ModelSerializer):
        name = serializers.PrimaryKeyRelatedField(
            queryset=Item.objects.all()
        )

        class Meta:
            model = OrderItem
            fields = ['name', 'quantity']

    item = TempOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['pk', 'item', 'total']

    def create(self, validated_data):
        item_data = validated_data.pop('item')
        validated_data['assigned'] = self.context.get('request').user

        with transaction.atomic():
            transaction_instance = Order.objects.create(**validated_data)
            for item in item_data:
                transaction_instance.item.create(**item)

        return transaction_instance
