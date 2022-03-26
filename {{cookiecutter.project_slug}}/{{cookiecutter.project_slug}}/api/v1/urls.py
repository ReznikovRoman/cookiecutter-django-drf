from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('schema/', include('api.v1.schema.urls')),

    path('auth/', include('api.v1.auth.urls')),
]
