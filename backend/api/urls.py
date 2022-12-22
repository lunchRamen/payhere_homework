from django.urls import include, path

from .views import AccountBookViewSet

urlpatterns = [
    path('users/', include('dj_rest_auth.urls')),
    path('users/signup/', include('dj_rest_auth.registration.urls')),
    path(
        "accountbook/",
        AccountBookViewSet.as_view({'post':'create', 'get': 'list'}),
        name="accountbooks",
    ),
    path(
        'accountbook/<int:accountbook_id>',
        AccountBookViewSet.as_view({'patch':'update', 'get':'retrieve', 'delete':'destroy'}),
        name = "accountbook",
    ),
]