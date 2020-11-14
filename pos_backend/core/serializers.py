from rest_framework import serializers
from .models import Item, Variant


class ItemSerializer(serializers.ModelSerializer):
    class TempVariantSerializer(serializers.ModelSerializer):
        name = serializers.StringRelatedField()

        class Meta:
            model = Variant
            fields = ['name', 'type']

    variant = TempVariantSerializer(many=True, read_only=True)
    product = serializers.StringRelatedField()

    class Meta:
        model = Item
        fields = ['pk', 'product', 'price', 'variant']
