from django.test import TestCase
from django.contrib.auth.models import User, Permission, Group, ContentType
from .models import Product, VariantType, Item, Variant

# Create your tests here.


def setup_user_cashier():
    user = User.objects.create_user(
        username='user_cashier',
        email='user_cashier@user.com',
        password='password_cashier'
    )
    group = Group.objects.create(
        name="Cashier"
    )
    user.groups.add(group)

    content_type_list = ('product', 'varianttype', 'item', 'variant')
    for content_type_model in content_type_list:
        content_type = ContentType.objects.get(
            app_label='core',
            model=content_type_model
            )
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            group.permissions.add(permission)

    return user


def setup_items():
    product = []
    product.append(Product.objects.create(
        name="Lagundi Syrup"
    ))
    product.append(Product.objects.create(
        name="Johnson Baby Powder"
    ))

    variant_type = []
    variant_type.append(VariantType.objects.create(
        type="Size"
    ))
    variant_type.append(VariantType.objects.create(
        type="Volume"
    ))
    variant_type.append(VariantType.objects.create(
        type="Flavor"
    ))

    item = []
    item.append(Item.objects.create(
        product=product[0],
        price=100,
    ))
    item.append(Item.objects.create(
        product=product[1],
        price=100,
    ))
    item[0].variant.create(
        name=variant_type[1],
        type="100ML"
    )
    item[0].variant.create(
        name=variant_type[2],
        type="Orange"
    )

    item[1].variant.create(
        name=variant_type[0],
        type="100G"
    )
    item[1].variant.create(
        name=variant_type[2],
        type="Blueberry"
    )

    return item
