from django.urls import path
from .views import LoginView, RegisterView , GoogleAuthView, GoogleAuthCallbackView,OrderView,ProductView,ProductFeatureView,CategoryView,FeatureView,CommentView,ImageView,UserView, ProductFilterView, ProductPaginationView

app_name = 'app'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('google/', GoogleAuthView.as_view(), name='google'),
    path('callback/', GoogleAuthCallbackView.as_view(), name='callback'),
    path("product/<int:pk>/", ProductView.as_view(), name='product'),
    path("category/<int:pk>/", CategoryView.as_view(), name='category'),
    path("product-feature/<int:pk>/", ProductFeatureView.as_view(), name='product-feature'),
    path("feature/<int:pk>/", FeatureView.as_view(), name='feature'),
    path("comment/<int:pk>/", CommentView.as_view(), name='comment'),
    path("image/<int:pk>/", ImageView.as_view(), name='image'),
    path("user/<int:pk>/", UserView.as_view(), name='user'),
    path('order/<int:pk>/', OrderView.as_view(), name='order'),
    path('products/', ProductFilterView.as_view(), name='product-filter'),
    path('product/', ProductPaginationView.as_view(), name='product-pagination'),
]