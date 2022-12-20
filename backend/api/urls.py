from django.urls import include, path

urlpatterns = [
    path('users/', include('dj_rest_auth.urls')),
    path('users/signup/', include('dj_rest_auth.registration.urls'))
]