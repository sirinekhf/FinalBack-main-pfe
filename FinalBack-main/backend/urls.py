from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.API.urls')),
    path('users/', include('users.urls')),
    path('partners/', include('partners.urls')),
    path('orders/', include('panier.urls')),
    path('products/', include('products.urls')),
    path('pay/', include('epay.urls')),
    path('ML/', include('ML.urls')),
]
