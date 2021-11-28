from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import include, path


urlpatterns = [
    path('', include('rest_framework.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
