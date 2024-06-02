from django.test import TestCase
from shop.models import Product, ProductFeature, Category, Image, Feature, Comment, User
from django.utils import timezone

# Create your tests here.
class FeatureTest(TestCase):
    def setUp(self):
        self.feature = Feature.objects.create(
            name='Test Feature',
            size=10,
            weight=5,
            color='Red',
            material='Metal'
        )
    def test_feature_fiels(self):
        self.assertEqual(self.feature.name, 'Test Feature')
        self.assertEqual(self.feature.size, 10)
        self.assertEqual(self.feature.weight, 5)
        self.assertEqual(self.feature.color, 'Red')
        self.assertEqual(self.feature.material, 'Metal')

class ProductFeatureTest(TestCase):
    def setUp(self):
        self.feature1 = Feature.objects.create(name='Feature 1')
        self.feature2 = Feature.objects.create(name='Feature 2')
        self.product_feature = ProductFeature.objects.create(value=5)

    def test_product_feature_value(self):
        self.assertEqual(self.product_feature.value, 5)
    def test_product_feature_features(self):
        self.product_feature.feature.add(self.feature1,self.feature2 )
        self.assertIn(self.feature1, self.product_feature.feature.all())
        self.assertIn(self.feature2, self.product_feature.feature.all())
        self.assertEqual(self.product_feature.feature.count(), 2)

class ImageTest(TestCase):
    def setUp(self):
        self.image = Image.objects.create(image='path/to/image.jpg')
    def test_image_field(self):
        self.assertEqual(self.image.image, 'path/to/image.jpg')

class UserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')

    def test_user_email(self):
        self.assertEqual(self.user.email, 'test@example.com')

class CategoryTest(TestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(title='ParentCategory', slug='parent-category', status=True)
        self.child_category = Category.objects.create(parent=self.parent_category, title='Child Category', slug='child-category', status=False)

    def test_category_fields(self):
        self.assertEqual(self.parent_category.title, 'ParentCategory')
        self.assertEqual(self.parent_category.slug, 'parent-category')
        self.assertTrue(self.parent_category.status)
        self.assertIsNone(self.parent_category.parent)
        self.assertEqual(self.child_category.title, 'Child Category')
        self.assertEqual(self.child_category.slug, 'child-category')
        self.assertFalse(self.child_category.status)
        self.assertEqual(self.child_category.parent, self.parent_category)
        self.assertIn(self.child_category, self.parent_category.children.all())

class ProductTest(TestCase):
    def setUp(self):
        category = Category.objects.create(title='Category 1', slug='category-1', status=True)
        image = Image.objects.create(image='path/to/image.jpg')
        feature = Feature.objects.create(name='Feature 1', size=10, weight=20, color='red',material='wood')
        product_feature = ProductFeature.objects.create(value=5)
        product_feature.feature.add(feature)
        self.product = Product.objects.create(name='Product 1',slug='product-1', description='product description', price=100, category=category, image=image)
        self.product.feature.add(product_feature)

    def test_product_fields(self):
        self.assertEqual(self.product.name, 'Product 1')
        self.assertEqual(self.product.slug, 'product-1')
        self.assertEqual(self.product.description, 'product description')
        self.assertEqual(self.product.price, 100)
        self.assertEqual(self.product.category.title, 'Category 1')
        self.assertEqual(self.product.image.image, 'path/to/image.jpg')

    def test_product_features(self):
        self.assertEqual(self.product.feature.count(), 1)
        product_feature = self.product.feature.first()
        self.assertEqual(product_feature.value, 5)
        self.assertEqual(product_feature.feature.first().name, 'Feature 1')
        self.assertEqual(product_feature.feature.first().size, 10)
        self.assertEqual(product_feature.feature.first().weight, 20)
        self.assertEqual(product_feature.feature.first().color, 'red')
        self.assertEqual(product_feature.feature.first().material, 'wood')

class CommentTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser',email='test@example.com')
        product = Product.objects.create(name='Test Product', slug='test-product', description='product description',price=100)
        self.comment = Comment.objects.create(writer=user, text='Test comment', date=timezone.now(), product=product)

    def test_comment_fields(self):
        self.assertEqual(self.comment.writer.username, 'testuser')
        self.assertEqual(self.comment.text, 'Test comment')
        self.assertIsNotNone(self.comment.date)
        self.assertEqual(self.comment.product.name, 'Test Product')