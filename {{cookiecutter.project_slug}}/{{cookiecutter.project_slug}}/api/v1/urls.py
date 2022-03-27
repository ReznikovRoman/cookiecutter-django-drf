from django.urls import include, path


app_name = 'api'

urlpatterns = [
    path('schema/', include('{{cookiecutter.project_slug}}.api.v1.schema.urls')),

    path('auth/', include('{{cookiecutter.project_slug}}.api.v1.auth.urls')),
]
