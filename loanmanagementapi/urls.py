from django.urls import path, include
from .views import*
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# # router.register(r'loans', LoanViewSet, basename='loan'),RefreshTokenView
# router.register(r'LoginViewSet', LoginViewSet, basename='login')
# router.register(r'UserCreateView', UserCreateView, basename='UsercreateView')
# router.register(r'RefreshTokenView', RefreshTokenView, basename='RefreshTokenView')
# router.register(r'LoanView', LoanView, basename='LoanView')


# urlpatterns = [
#     path('', include(router.urls)),
#     # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
# ]




urlpatterns = [

    path('LoginAPIView/', LoginAPIView.as_view(), name='login'),
    path('UserCreateView/', UserCreateView.as_view(), name='UserCreateView'),
    path('RefreshTokenView/', RefreshTokenView.as_view(), name='RefreshTokenView'),
    path('LoanView/', LoanView.as_view(), name='LoanView'),
    
    # # JWT Token URLs
   ]