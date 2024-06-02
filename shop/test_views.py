from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Feature, User, Image, ProductFeature, Category, Product, Comment
from io import BytesIO
from PIL import Image as PILImage
from django.core.files.uploadedfile import SimpleUploadedFile


class FeatureViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.feature = Feature.objects.create(name='Feature 1', size=10, weight=5, color='Red', material='Metal')

    def test_get_feature(self):
        url = reverse('app:feature', kwargs={'pk': self.feature.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Feature 1')
        self.assertEqual(response.data['size'], 10)
        self.assertEqual(response.data['weight'], 5)
        self.assertEqual(response.data['color'], 'Red')
        self.assertEqual(response.data['material'], 'Metal')


    def test_update_feature(self):
        url = reverse('app:feature', kwargs={'pk': self.feature.pk})
        data = {
            'name': 'Updated Feature',
            'size': 20,
            'weight': 10,
            'color': 'Blue',
            'material': 'Plastic'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Feature')
        self.assertEqual(response.data['size'], 20)
        self.assertEqual(response.data['weight'], 10)
        self.assertEqual(response.data['color'], 'Blue')
        self.assertEqual(response.data['material'], 'Plastic')
        #self.assertEqual(response.data['slug'], 'slug')


    def test_create_feature(self):
        url = reverse('app:feature', kwargs={'pk': self.feature.pk})
        data = {
            'name': 'New Feature',
            'size': 15,
            'weight': 8,
            'color': 'Green',
            'material': 'Wood'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Feature')
        self.assertEqual(response.data['size'], 15)
        self.assertEqual(response.data['weight'], 8)
        self.assertEqual(response.data['color'], 'Green')
        self.assertEqual(response.data['material'], 'Wood')

    #def test_feature_model_delete(self):
    #    feature = self.test_create_feature()
    #    pk = feature.pk
    #    get_feature = feature.objects.get(pk=feature.pk)
    #    del_pay = get_feature.delete()
    #    self.assertFalse(Feature.objects.filter(pk=pk).exists())


class UserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', email='test@example.com')

    def test_get_user(self):
        url = reverse('app:user', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com') 

    def test_update_user(self):
        url = reverse('app:user', kwargs={'pk': self.user.pk})
        data = {
            'username': 'Updateduser',
            'email': 'updated@example.com',
            'password': '1234'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'Updateduser')
        self.assertEqual(response.data['email'], 'updated@example.com')
        self.assertEqual(response.data['password'], '1234') 

    #def test_delete_user(self):
    #    url = reverse('category:user', kwargs={'pk': self.user.pk})
    #    response = self.client.delete(url)
    #    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #    self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        
    def test_create_user(self):
        url = reverse('app:user', kwargs={'pk': self.user.pk})
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': '12345'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertEqual(response.data['email'], 'new@example.com')
        self.assertEqual(response.data['password'], '12345')
    
class ProductFeatureViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product_feature = ProductFeature.objects.create(value=10)

    def test_get_product_feature(self):
        url = reverse('app:product-feature', kwargs={'pk': self.product_feature.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], 10)

    def test_update_product_feature(self):
        url = reverse('app:product-feature', kwargs={'pk': self.product_feature.pk})
        feature1 = Feature.objects.create(name='Feature 1', size=10, weight=5, color='Red', material='Wood')
        feature2 = Feature.objects.create(name='Feature 2', size=20, weight=8, color='Blue', material='Metal')
        data = {
            'value': 20,
            'feature':[feature1.pk, feature2.pk]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], 20)
        self.assertEqual(response.data['feature'], [feature1.pk, feature2.pk]) 

    #def test_delete_product_feature(self):
    #    url = reverse('category:product-feature', kwargs={'pk': self.product_feature.pk})
    #    response = self.client.delete(url)
    #    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #    self.assertFalse(ProductFeature.objects.filter(pk=self.product_feature.pk).exists())


    def test_create_product_feature(self):
        url = reverse('app:product-feature', kwargs={'pk': self.product_feature.pk})
        feature1 = Feature.objects.create(name='Feature 1', size=10, weight=5, color='Red', material='Wood')
        feature2 = Feature.objects.create(name='Feature 2', size=20, weight=8, color='Blue', material='Metal')
        data = {
            'value': 30,
            'feature':[feature1.pk, feature2.pk]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['value'], 30)
        self.assertEqual(response.data['feature'], [feature1.pk, feature2.pk])


class CategoryViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(title='Category 1', slug='category-1')

    def test_get_category(self):
        url = reverse('app:category', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Category 1')

    def test_update_category(self):
        url = reverse('app:category', kwargs={'pk': self.category.pk})
        data = {
            'title': 'Updated Category',
            'slug': 'updated-category'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Category')
        self.assertEqual(response.data['slug'], 'updated-category')

    #def test_delete_category(self):
    #    url = reverse('category:category', kwargs={'pk': self.category.pk})
    #    response = self.client.delete(url)
    #    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #    self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())

    def test_create_category(self):
        url = reverse('app:category', kwargs={'pk': self.category.pk})
        data = {
            'title': 'New Category',
            'slug': 'new-category'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Category')
        self.assertEqual(response.data['slug'], 'new-category')

class ImageViewTest(TestCase):
    @override_settings(MEDIA_ROOT='images/')
    def setUp(self):
        self.client = APIClient()
        # ایجاد یک تصویر ساده برای تست
        image = PILImage.new('RGB', size=(100, 100))
        # ذخیره تصویر در حافظه موقت به صورت BytesIO
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        # ایجاد یک فایل آپلود شده به وسیله تصویر ساخته شده
        uploaded_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )
        # ایجاد شیء Image با استفاده از فایل آپلود شده
        self.image = Image.objects.create(image=uploaded_image)

    def test_get_image(self):
        url = reverse('app:image', kwargs={'pk': self.image.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # دریافت بایت‌های تصویر از پاسخ
        image_bytes = response.content
        # اعتبارسنجی بایت‌های تصویر
        self.assertIsNotNone(image_bytes)

    def test_update_image(self):
        url = reverse('app:image', kwargs={'pk': self.image.pk})
        image = PILImage.new('RGB', size=(100, 100))
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        updated_image = SimpleUploadedFile(
            name='updated_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )
        data = {
            'image': updated_image
        }
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_image(self):
        url = reverse('app:image', kwargs={'pk': self.image.pk})
        image = PILImage.new('RGB', size=(100, 100))
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        new_image = SimpleUploadedFile(
            name='new_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )
        data = {
            'image': new_image
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ProductViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(name='Test Product', slug='test-product', description='This is a test product.', price=99)

    def test_get_product(self):
        url = reverse('app:product', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')
        # Add more assertions for other fields if needed

    def test_create_product(self):
        url = reverse('app:product', args=[self.product.pk])
        feature1 = Feature.objects.create(name='Feature 1', size=10, weight=5, color='Red', material='Wood')
        feature2 = Feature.objects.create(name='Feature 2', size=20, weight=8, color='Blue', material='Metal')

        product_feature1 = ProductFeature.objects.create(value=1)
        product_feature1.feature.add(feature1)

        product_feature2 = ProductFeature.objects.create(value=2)
        product_feature2.feature.add(feature2)

        product_data = {
            'name': 'Test Product',
            'slug': 'test-product',
            'description': 'This is a test product.',
            'price': 99,
            'feature': [product_feature1.pk, product_feature2.pk],
            'category': '',
            'image': '',
        }

        response = self.client.post(url, product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Product')
        self.assertEqual(response.data['slug'], 'test-product')
        self.assertEqual(response.data['description'], 'This is a test product.')
        self.assertEqual(response.data['price'],99)
        self.assertEqual(response.data['feature'], [product_feature1.pk, product_feature2.pk])
        self.assertEqual(response.data['category'], None)
        self.assertEqual(response.data['image'], None)

    def test_update_product(self):
        url = reverse('app:product', args=[self.product.pk])
        feature1 = Feature.objects.create(name='Feature 1', size=10, weight=5, color='Red', material='Wood')
        feature2 = Feature.objects.create(name='Feature 2', size=20, weight=8, color='Blue', material='Metal')

        product_feature1 = ProductFeature.objects.create(value=1)
        product_feature1.feature.add(feature1)

        product_feature2 = ProductFeature.objects.create(value=2)
        product_feature2.feature.add(feature2)

        product_data = {
            'name': 'Updated Product',
            'slug': 'updated-product',
            'description': 'This is an updated product.',
            'price': 99,
            'feature': [product_feature1.pk, product_feature2.pk],
            'category': '',
            'image': '',
        }

        response = self.client.put(url, product_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Product')
        self.assertEqual(response.data['slug'], 'updated-product')
        self.assertEqual(response.data['description'], 'This is an updated product.')
        self.assertEqual(response.data['price'],99)
        self.assertEqual(response.data['feature'], [product_feature1.pk, product_feature2.pk])
        self.assertEqual(response.data['category'], None)
        self.assertEqual(response.data['image'], None)


class CommentViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(name='Test Product', slug='test-product', description='This is a test product.', price=99)
        self.comment = Comment.objects.create(writer=self.user, text='This is a test comment.', product=self.product)

    def test_get_comment(self):
        url = reverse('app:comment', args=[self.comment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(response.data['writer'], self.user)
        self.assertEqual(response.data['text'], 'This is a test comment.')
        #self.assertEqual(response.data['product'], self.product)

    def test_create_comment(self):
        url = reverse('app:comment', args=[self.comment.pk])
        user = User.objects.create(username='user', email='test@example.com')
        feature = Feature.objects.create(name='Feature 1', size=10, weight=5, color='Red', material='Wood')
        product_feature = ProductFeature.objects.create(value=1)
        product_feature.feature.add(feature)
        product = Product.objects.create(name='Test Product', slug='test-product', description='This is a test product.', price=99)
        product.feature.add(product_feature)

        comment_data = {
            'writer': user.pk,
            'text': 'This is a test comment.',
            'date': '2022-01-01T00:00:00Z',
            'product': product.pk,
        }

        response = self.client.post(url, comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(response.data['writer'], user.pk)
        #self.assertEqual(response.data['text'], 'This is a test comment.')
        #self.assertEqual(response.data['product'], self.product.pk)

    def test_update_comment(self):
        url = reverse('app:comment', args=[self.comment.pk])
        user = User.objects.create(username='user', email='test@example.com')
        feature = Feature.objects.create(name='Feature 1', size=10, weight=5, color='Red', material='Wood')
        product_feature = ProductFeature.objects.create(value=1)
        product_feature.feature.add(feature)
        product = Product.objects.create(name='Test Product', slug='test-product', description='This is a test product.', price=99)
        product.feature.add(product_feature)

        comment_data = {
            'writer': user.pk,
            'text': 'This is a test comment.',
            'date': '2022-01-01T00:00:00Z',
            'product': product.pk,
        }

        response = self.client.put(url, comment_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions to check if the comment is updated correctly

    #def test_delete_comment(self):
    #    url = reverse('category:comment', args=[self.comment.pk])
    #    response = self.client.delete(url)
    #    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #    self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())