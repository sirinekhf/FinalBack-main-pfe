from . import views
from django.urls import path

from .views import SubmitOrderView, getCommandeOfUser, getCommandeDetails, updatesaleorderView, sendemail, \
    getAllCommande, getCommandeById
urlpatterns = [

    path('sendemail/', sendemail),
    path('createorder', SubmitOrderView.as_view()),
    path('getCmdByUser/<str:user_email>', getCommandeOfUser),
    path('getCmdById/<int:cmd_id>', getCommandeDetails),
    path('getCmd/<int:cmd_id>', getCommandeById),
    path('saleorder/<int:id>/user/<int:user_id>/update/', updatesaleorderView.as_view(), name='updatesaleorder'),
    path('getallcmd/', getAllCommande ),
    path('getbestseller/', views.get_best_sellers ),
    path('getdepot/', views.get_depot ),

]
