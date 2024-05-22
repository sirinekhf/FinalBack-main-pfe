from django.urls import path
from . import views
urlpatterns = [
    path('register', views.registerView.as_view()),
    path('user', views.userView.as_view()),
    path('comerciaux', views.getComercial , name='get_comercials'),
    path('clients', views.getUsers, name='user'),
    path('changeaccess/<int:id>', views.changeaccess ),
    path('getuser/<int:id>', views.getuserbyid),
]
