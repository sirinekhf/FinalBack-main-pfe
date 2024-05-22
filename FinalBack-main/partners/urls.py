from . import views
from django.urls import path
urlpatterns = [
    #path('api/usersImport', views.insertIntoMyDB),
    #path('api/insertall', views.insert),
    path('importcountry', views.importCountry),
    path('importstate', views.importState),
    path('importlocalite', views.importLocalite),
    path('edit', views.editPartner.as_view()),
    path('getpartnerfromuser/<int:user_id>', views.getPartnerfromUser),
    path('getcommune/<int:code>', views.getCommune),
    path('getwilaya', views.getWilaya),
    path('getwilayabyid/<int:id>', views.getWilayaById),
    path('getcommunebyid/<int:id>', views.getCommuneById)
]