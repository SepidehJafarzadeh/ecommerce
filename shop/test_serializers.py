from django.test import TestCase, override_settings
from .models import Feature, ProductFeature, Product, User
from .serializers import ProductSerialiser , FeatureSerialiser, ProductFeatureSerialiser, ImageSerialiser, UserSerialiser, CategorySerialiser, CommentSerialiser
from django.core.files.uploadedfile import SimpleUploadedFile

class FeatureSerializerTest(TestCase):
    def test_feature_serializer(self):
        feature_data = {
            'name': 'Test Feature',
            'size': 10,
            'weight': 5,
            'color': 'Red',
            'material': 'Wood',
        }
        serializer = FeatureSerialiser(data=feature_data)
        self.assertTrue(serializer.is_valid())
        feature = serializer.save()

        self.assertEqual(feature.name, 'Test Feature')
        self.assertEqual(feature.size, 10)
        self.assertEqual(feature.weight, 5)
        self.assertEqual(feature.color, 'Red')
        self.assertEqual(feature.material, 'Wood')

class UserSerializerTest(TestCase):
    def test_user_serializer(self):
        user_data = {
            'username':'testuser',
            'email':'test@example.com',
            'password':'testpassword',
        }
        serializer = UserSerialiser(data=user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.password,'testpassword')

class ProductFeatureSerializerTest(TestCase):
    def test_product_feature_serializer(self):
        feature1 = Feature.objects.create(name='Feature 1', size=10, weight=5, color='Red', material='Wood')
        feature2 = Feature.objects.create(name='Feature 2', size=20, weight=8, color='Blue', material='Metal')

        product_feature_data = {
            'value': 15,
            'feature': [feature1.pk, feature2.pk],
        }
        serializer = ProductFeatureSerialiser(data=product_feature_data)
        self.assertTrue(serializer.is_valid())
        product_feature = serializer.save()

        self.assertEqual(product_feature.value, 15)
        self.assertEqual(product_feature.feature.count(), 2)
        self.assertIn(feature1, product_feature.feature.all())
        self.assertIn(feature2, product_feature.feature.all())

#class ImageSerializerTest(TestCase):
    #@override_settings(MEDIA_ROOT='images/')
    #def test_image_serializer(self):
        # Create a test image file
        #image_file = SimpleUploadedFile(
        #    name='aa.webp',
        #    content=open('images/aa.webp', 'rb').read(),
        #    content_type='image/jpeg'
        #)

        #image_data = {
        #    'image': image_file,
        #}
        #serializer = ImageSerialiser(data=image_data)
        #self.assertTrue(serializer.is_valid())
        #image = serializer.save()

        #self.assertIsNotNone(image.image)
        #self.assertTrue(image.image.name.startswith('images/'))
        #self.assertTrue(image.image.url.startswith('images/'))

class CategorySerializerTest(TestCase):
    def test_category_serializer(self):
        category_data = {
            'parent': None,
            'title': 'Test Category',
            'slug': 'test-category',
            'status': True,
        }
        serializer = CategorySerialiser(data=category_data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()

        self.assertIsNone(category.parent)
        self.assertEqual(category.title, 'Test Category')
        self.assertEqual(category.slug, 'test-category')
        self.assertEqual(category.status, True)

class ProductSerializerTest(TestCase):
    def test_product_serializer(self):
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
            'category': None,
            'image': None,
        }
        serializer = ProductSerialiser(data=product_data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()

        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.slug, 'test-product')
        self.assertEqual(product.description, 'This is a test product.')
        self.assertEqual(product.price, 99)
        self.assertListEqual(list(product.feature.all()), [product_feature1, product_feature2])
        self.assertIsNone(product.category)
        self.assertIsNone(product.image)

class CommentSerializerTest(TestCase):
    def test_comment_serializer(self):
        user = User.objects.create(username='testuser', email='test@example.com')
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
        serializer = CommentSerialiser(data=comment_data)
        self.assertTrue(serializer.is_valid())
        comment = serializer.save()

        self.assertEqual(comment.writer, user)
        self.assertEqual(comment.text, 'This is a test comment.')
        self.assertEqual(comment.date.isoformat(), '2022-01-01T00:00:00+00:00')
        self.assertEqual(comment.product, product)