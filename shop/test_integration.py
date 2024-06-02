from rest_framework.test import APIClient, APITestCase, override_settings
from django.urls import reverse
from rest_framework import status
from django.test import TestCase, TransactionTestCase
from .models import Feature, ProductFeature, User, Image, Category, Product, Comment
from io import BytesIO
from PIL import Image as PILImage
from django.core.files.uploadedfile import SimpleUploadedFile



class FeatureIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.feature = Feature.objects.create(name='Feature 1', size=10, weight=5, color='Red', material='Metal')

    def test_feature_crud_operations(self):
        # Create feature
        create_url = reverse('app:feature', kwargs={'pk': self.feature.pk})
        create_data = {
            'name': 'New Feature',
            'size': 15,
            'weight': 8,
            'color': 'Green',
            'material': 'Wood'
        }
        create_response = self.client.post(create_url, create_data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data['name'], 'New Feature')
        self.assertEqual(create_response.data['size'], 15)
        self.assertEqual(create_response.data['weight'], 8)
        self.assertEqual(create_response.data['color'], 'Green')
        self.assertEqual(create_response.data['material'], 'Wood')

        new_feature_id = create_response.data['id']
        
        # Retrieve feature
        retrieve_url = reverse('app:feature', kwargs={'pk': new_feature_id})
        retrieve_response = self.client.get(retrieve_url)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_response.data['name'], 'New Feature')
        self.assertEqual(retrieve_response.data['size'], 15)
        self.assertEqual(retrieve_response.data['weight'], 8)
        self.assertEqual(retrieve_response.data['color'], 'Green')
        self.assertEqual(retrieve_response.data['material'], 'Wood')

        # Update feature
        update_url = reverse('app:feature', kwargs={'pk': new_feature_id})
        update_data = {
            'name': 'Updated Feature',
            'size': 20,
            'weight': 10,
            'color': 'Blue',
            'material': 'Plastic'
        }
        update_response = self.client.put(update_url, update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['name'], 'Updated Feature')
        self.assertEqual(update_response.data['size'], 20)
        self.assertEqual(update_response.data['weight'], 10)
        self.assertEqual(update_response.data['color'], 'Blue')
        self.assertEqual(update_response.data['material'], 'Plastic')

        # Delete feature
        #delete_url = reverse('category:feature', kwargs={'pk': new_feature_id})
        #delete_response = self.client.delete(delete_url)
        #self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        #self.assertFalse(Feature.objects.filter(pk=new_feature_id).exists())




class ProductFeatureIntegrationTest(TransactionTestCase):
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
            'feature': [feature1.pk, feature2.pk]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], 20)
        self.assertEqual(response.data['feature'], [feature1.pk, feature2.pk])

    def test_create_product_feature(self):
        url = reverse('app:product-feature', kwargs={'pk': self.product_feature.pk})
        feature1 = Feature.objects.create(name='Feature 1', size=10, weight=5, color='Red', material='Wood')
        feature2 = Feature.objects.create(name='Feature 2', size=20, weight=8, color='Blue', material='Metal')
        data = {
            'value': 30,
            'feature': [feature1.pk, feature2.pk]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['value'], 30)
        self.assertEqual(response.data['feature'], [feature1.pk, feature2.pk])




class UserViewIntegrationTest(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user('testuser', 'test@example.com', 'password')

    def create_user(self, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return user

    def test_get_user(self):
        url = reverse('app:user', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
        #self.assertEqual(response.data['password'], 'password')

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




class ImageViewIntegrationTest(TransactionTestCase):
    @override_settings(MEDIA_ROOT='images/')
    def setUp(self):
        self.client = APIClient()
        self.image = self.create_image()

    def create_image(self):
        image = PILImage.new('RGB', size=(100, 100))
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        uploaded_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )
        image = Image.objects.create(image=uploaded_image)
        return image

    def test_get_image(self):
        url = reverse('app:image', kwargs={'pk': self.image.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.content)

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



class CategoryIntegrationTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Category 1', slug='category-1')

    def test_get_category(self):
        url = reverse('app:category', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Category 1')
        self.assertEqual(response.data['slug'], 'category-1')

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




class ProductIntegrationTest(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Test Product', slug='test-product', description='This is a test product.', price=99)
        self.feature1 = Feature.objects.create(name='Feature 1', size=10, weight=5, color='Red', material='Wood')
        self.feature2 = Feature.objects.create(name='Feature 2', size=20, weight=8, color='Blue', material='Metal')
        self.product_feature1 = ProductFeature.objects.create(value=1)
        self.product_feature1.feature.add(self.feature1)
        self.product_feature2 = ProductFeature.objects.create(value=2)
        self.product_feature2.feature.add(self.feature2)
        self.category = Category.objects.create(title='Test Category', slug='test-category', status=True)
        self.image = Image.objects.create(image='test_image.jpg')

    def test_get_product(self):
        url = reverse('app:product', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')
        self.assertEqual(response.data['slug'], 'test-product')
        self.assertEqual(response.data['description'], 'This is a test product.')
        self.assertEqual(response.data['price'],99)
        #self.assertEqual(response.data['feature'], [self.product_feature1.pk, self.product_feature2.pk])
        #self.assertEqual(response.data['category'], self.category.pk)
        #self.assertEqual(response.data['image'], self.image.pk)

    def test_create_product(self):
        url = reverse('app:product', args=[self.product.pk])
        product_data = {
            'name': 'New Product',
            'slug': 'new-product',
            'description': 'This is a new product.',
            'price': 50,
            'feature': [self.product_feature1.pk, self.product_feature2.pk],
            'category': self.category.pk,
            'image': self.image.pk,
        }
        response = self.client.post(url, product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Product')
        self.assertEqual(response.data['slug'], 'new-product')
        self.assertEqual(response.data['description'], 'This is a new product.')
        self.assertEqual(response.data['price'],50)
        self.assertEqual(response.data['feature'], [self.product_feature1.pk, self.product_feature2.pk])
        self.assertEqual(response.data['category'], self.category.pk)
        self.assertEqual(response.data['image'], self.image.pk)



    def test_update_product(self):
        url = reverse('app:product', args=[self.product.pk])
        product_data = {
            'name': 'Updated Product',
            'slug': 'updated-product',
            'description': 'This is an updated product.',
            'price': 150,
            'feature': [self.product_feature1.pk, self.product_feature2.pk],
            'category': self.category.pk,
            'image': self.image.pk,
        }
        response = self.client.put(url, product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Product')
        self.assertEqual(response.data['slug'], 'updated-product')
        self.assertEqual(response.data['description'], 'This is an updated product.')
        self.assertEqual(response.data['price'], 150)
        self.assertEqual(response.data['feature'], [self.product_feature1.pk, self.product_feature2.pk])
        self.assertEqual(response.data['category'], self.category.pk)
        self.assertEqual(response.data['image'], self.image.pk)



class CommentIntegrationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(name='Test Product', slug='test-product', description='This is a test product.', price=99)
        self.comment = Comment.objects.create(writer=self.user, text='This is a test comment.', product=self.product)

    def test_get_comment(self):
        url = reverse('app:comment', args=[self.comment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'This is a test comment.')
        # Add more assertions for other fields if needed

    def test_create_comment(self):
        url = reverse('app:comment',  args=[self.comment.pk])
        user = User.objects.create(username='user', email='test@example.com')

        comment_data = {
            'writer': user.pk,
            'text': 'This is a test comment.',
            'product': self.product.pk,
        }

        response = self.client.post(url, comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['writer'], user.pk)
        self.assertEqual(response.data['text'], 'This is a test comment.')
        self.assertEqual(response.data['product'], self.product.pk)

    def test_update_comment(self):
        url = reverse('app:comment', args=[self.comment.pk])
        user = User.objects.create(username='user', email='test@example.com')

        comment_data = {
            'writer': user.pk,
            'text': 'This is a test comment.',
            'product': self.product.pk,
        }

        response = self.client.put(url, comment_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['writer'], user.pk)
        self.assertEqual(response.data['text'], 'This is a test comment.')
        self.assertEqual(response.data['product'], self.product.pk)

    #def test_delete_comment(self):
    #    url = reverse('category:comment', args=[self.comment.pk])
    #    response = self.client.delete(url)
    #    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #    self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())