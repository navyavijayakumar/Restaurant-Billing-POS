from django.urls import path
from rbs import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken

router=DefaultRouter()
router.register("table",views.TableViewSetView,basename="tables")
router.register('category',views.CategoryViewSet,basename="category")
router.register('products',views.ProductViewSet,basename="products")

urlpatterns=[
    path("category/<int:pk>/products/",views.ProductCreateView.as_view()),
    path("users/",views.UserCreateView.as_view()),
    path("token/",ObtainAuthToken.as_view()),
]+ router.urls