from shop.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from ecommerce import settings
import requests
import random
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Category, Feature, ProductFeature, Comment, Image, Order
from django.http import Http404
from .serializers import ProductSerialiser,UserSerialiser, CategorySerialiser, FeatureSerialiser, ProductFeatureSerialiser, CommentSerialiser, ImageSerialiser, OrderSerialiser



# Create your views here.
class ProductFilterView(APIView):
    def get(self, request):
        name = request.query_params.get('name', None)
        title = request.query_params.get('title', None)

        products = Product.objects.all()

        try:
            if name:
                products = products.filter(name__icontains=name)

            if title:
                category = Category.objects.filter(title__icontains=title).first()
                if category:
                    products = products.filter(category=category)

            serializer = ProductSerialiser(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)



class RegisterView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')
            if not username:
                return Response({'message': 'you must enter your username'}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(username=username).exists():
                return Response({'message':'your username is exist'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=username, password=password, email=email)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response({'message':'you have registered', 'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'message':'you did not register'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response({'message':'you have logged in','token':token}, status=status.HTTP_200_OK)
        else:
            return Response({'message':'you did not log in'}, status=status.HTTP_400_BAD_REQUEST)
        



class GoogleAuthView(APIView):
    def get(self, request):
        # Build the authorization URL
        base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
        redirect_uri = "http://127.0.0.1:8000/callback/"
        scope = 'email profile openid'
        state = ''.join(random.choice('') for _ in range(16))
        auth_url = f"{base_url}?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&state={state}"

        # Return the authorization URL as a JSON response
        return Response({'auth_url': auth_url})


class GoogleAuthCallbackView(APIView):

    def token_generator(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def get(self, request):
        # Get the authorization code from the request
        code = request.GET.get('code')

        # Exchange the authorization code for tokens
        token_url = 'https://oauth2.googleapis.com/token'
        redirect_uri = "http://127.0.0.1:8000/callback/"
        data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        response = requests.post(token_url, data=data)
        try:
            if response.status_code == 400:
                return Response(data='Login failed', status=status.HTTP_401_UNAUTHORIZED)

            access_token = response.json()['access_token']
            # Now you have the access_token, you can use it to make requests to Google APIs
            # For example, to get user info:
            user_info_response = requests.get('https://openidconnect.googleapis.com/v1/userinfo',
                                          headers={'Authorization': f'Bearer {access_token}'})
            user_info = user_info_response.json()
            # Extract user's email from the response
            user_email = user_info.get('email')
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)


        # Check if the user already exists
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            # User does not exist, create a new user
            user = User.objects.create_user(username=user_email, email=user_email, password=None)

        # Generate a JWT token for the user
        token = self.token_generator(user)

        return Response(data={'token': token}, status=status.HTTP_200_OK)



class OrderView(APIView):

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except  Order.DoesNotExist :
            raise Http404
        
    def get(self, request, pk, format=None):
        Order = self.get_object(pk)
        try:
            serializer = OrderSerialiser(Order)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk, format=None):
        Order = self.get_object(pk)
        serializer = OrderSerialiser(Order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        Order = self.get_object(pk)
        Order.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    
    def post(self, request,pk, format=None):
        serializer = OrderSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductView(APIView):

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except  Product.DoesNotExist :
            raise Http404
        
    def get(self, request, pk, format=None):
        Product = self.get_object(pk)
        try:
            serializer = ProductSerialiser(Product)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk, format=None):
        Product = self.get_object(pk)
        serializer = ProductSerialiser(Product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        Product = self.get_object(pk)
        Product.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    
    def post(self, request,pk, format=None):
        serializer = ProductSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except  Category.DoesNotExist :
            raise Http404
        
    def get(self, request, pk, format=None):
        Category = self.get_object(pk)
        try:
            serializer = CategorySerialiser(Category)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk, format=None):
        Category = self.get_object(pk)
        serializer = CategorySerialiser(Category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        Category = self.get_object(pk)
        Category.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    
    def post(self, request,pk, format=None):
        serializer = CategorySerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class ProductFeatureView(APIView):
    def get_object(self, pk):
        try:
            return ProductFeature.objects.get(pk=pk)
        except  ProductFeature.DoesNotExist :
            raise Http404
        
    def get(self, request, pk, format=None):
        ProductFeature = self.get_object(pk)
        try:
            serializer = ProductFeatureSerialiser(ProductFeature)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk, format=None):
        ProductFeature = self.get_object(pk)
        serializer = ProductFeatureSerialiser(ProductFeature, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        ProductFeature = self.get_object(pk)
        ProductFeature.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    
    def post(self, request,pk, format=None):
        serializer = ProductFeatureSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FeatureView(APIView):
    def get_object(self, pk):
        try:
            return Feature.objects.get(pk=pk)
        except  Feature.DoesNotExist :
            raise Http404
        
    def get(self, request, pk, format=None):
        Feature = self.get_object(pk)
        try:
            serializer = FeatureSerialiser(Feature)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk, format=None):
        Feature = self.get_object(pk)
        serializer = FeatureSerialiser(Feature, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        Feature = self.get_object(pk)
        Feature.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    
    def post(self, request,pk, format=None):
        serializer = FeatureSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class CommentView(APIView):
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except  Comment.DoesNotExist :
            raise Http404
        
    def get(self, request, pk, format=None):
        Comment = self.get_object(pk)
        try:
            serializer = CommentSerialiser(Comment)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk, format=None):
        Comment = self.get_object(pk)
        serializer = CommentSerialiser(Comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        Comment = self.get_object(pk)
        Comment.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    
    def post(self, request,pk, format=None):
        serializer = CommentSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageView(APIView):
    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except  Image.DoesNotExist :
            raise Http404
        
    def get(self, request, pk, format=None):
        Image = self.get_object(pk)
        try:
            serializer = ImageSerialiser(Image)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk, format=None):
        Image = self.get_object(pk)
        serializer = ImageSerialiser(Image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        Image = self.get_object(pk)
        Image.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    
    def post(self, request,pk, format=None):
        serializer = ImageSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class UserView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except  User.DoesNotExist :
            raise Http404
        
    def get(self, request, pk, format=None):
        User = self.get_object(pk)
        try:
            serializer = UserSerialiser(User)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk, format=None):
        User = self.get_object(pk)
        serializer = UserSerialiser(User, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        User = self.get_object(pk)
        User.delete()
        return Response(status.HTTP_204_NO_CONTENT)

    def post(self, request,pk, format=None):
        serializer = UserSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)