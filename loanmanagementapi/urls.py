from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
# router.register(r'loans', LoanViewSet, basename='loan'),
router.register(r'login', LoginViewSet, basename='login')
router.register(r'UsercreateView', UsercreateView, basename='UsercreateView')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]