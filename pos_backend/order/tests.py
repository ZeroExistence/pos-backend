from django.test import TestCase
from rest_framework.test import RequestsClient, APITestCase
from django.contrib.auth.models import User, Permission, Group, ContentType
from rest_framework import status
import json

from pos_backend.core.tests import setup_items
from .models import Order, OrderItem


# Create your tests here.

client = RequestsClient()
client.headers.update({'Content-Type': 'application/json'})

def setup_user_assistant():
    user = User.objects.create_user(
        username='user_assistant',
        email='user_assistant@user.com',
        password='password_assistant'
    )
    group = Group.objects.create(
        name="Assistant"
    )
    user.groups.add(group)

    content_type_list = ('order', 'orderitem',)
    for content_type_model in content_type_list:
        content_type = ContentType.objects.get(
            app_label='order',
            model=content_type_model
            )
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            group.permissions.add(permission)

    content_type_list_viewonly = ('item',)
    for content_type_model in content_type_list_viewonly:
        content_type = ContentType.objects.get(
            app_label='core',
            model=content_type_model
        )
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename='view_{0}'.format(content_type_model)
            )
        for permission in permissions:
            group.permissions.add(permission)

    return {'user': user, 'password': 'password_assistant'}


def setup_user_token(user):
    url = 'http://localhost:8000/api/token/'
    credentials = {
        "username": user['user'].username,
        "password": user['password']
        }

    response = client.post(
        url,
        data=json.dumps(credentials)
    )
    return response.json()


class OrderTest(TestCase):
    def setUp(self):
        self.items = setup_items()
        self.user = setup_user_assistant()

    def test_order_anonymous(self):
        order = Order.objects.create()
        for idx, item in enumerate(self.items, start=1):
            order.item.create(
                name=item,
                quantity=idx
            )
        self.assertIsNone(order, msg=order.pk)

    def test_order_items(self):
        self.client.force_login(user=self.user['user'])

        order = Order.objects.create(
            assigned=self.user['user']
        )
        for idx, item in enumerate(self.items, start=1):
            order.item.create(
                name=item,
                quantity=idx
            )
        self.assertEqual(order.total, 300)
        self.assertEqual(order.assigned, self.user['user'])
        self.assertEqual(order.item.all()[0].item_total, 100)
        self.assertEqual(order.item.all()[1].item_total, 200)


class OrderAPITest(APITestCase):
    def setUp(self):
        self.items = setup_items()
        self.user = setup_user_assistant()
        self.user_token = setup_user_token(self.user)

    def test_items_access(self):
        url = 'http://localhost:8000/api/item/'
        header = {"Authorization": "Bearer {0}".format(
            self.user_token['access']
            )}
        response = client.get(
            url,
            headers=header
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            msg=response.json()
            )

    def test_item_anonymous(self):
        url = 'http://localhost:8000/api/item/'
        response = client.get(
            url,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg=response.json()
            )

    def test_order_items_api(self):
        url = 'http://localhost:8000/api/order/'
        header = {"Authorization": "Bearer {0}".format(
            self.user_token['access']
            )}
        response = client.get(
            url,
            headers=header
        )
        data = {"item": []}
        for idx, item in enumerate(self.items, start=1):
            data['item'].append({
                "name": item.pk,
                "quantity": idx
            })
        response = client.post(
            url,
            data=json.dumps(data),
            headers=header
        )
        order = response.json()
        self.assertEqual(order.total, 300)
