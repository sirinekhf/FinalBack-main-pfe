from django.urls import path
from ML import views

urlpatterns = [
    path('frequent-itemsets/<int:product_id>', views.get_getItemsets, name='frequent-itemsets'),
    path('statistiques/CAbyProduct/<str:start_date>/<str:end_date>', views.getStatCAbyProduct, name='CAbyProduct'),
    path('statistiques/CmdbyState/<str:start_date>/<str:end_date>', views.getStatCmdbyState, name='CmdbyState'),
    path('statistiques/CAbyCategory/<str:start_date>/<str:end_date>', views.getStatCAbyCategory, name='CAbyCategory'),
    path('statistiques/getTopClients/<str:start_date>/<str:end_date>', views.get_top_clients, name='getTopClients'),
    path('statistiques/getTopProducts/<str:start_date>/<str:end_date>', views.get_top_products, name='getTopProducts'),
    path('statistiques/getTopCategories/<str:start_date>/<str:end_date>', views.get_top_categories, name='getTopCategories'),
    path('statistiques/getNbrNewClientsWeek', views.nbr_new_clients_week, name='getNbrNewClientsWeek'),
    path('statistiques/getTotalRevenueToday', views.total_revenue_today, name='getTotalRevenueToday'),
    path('statistiques/getNbrCmdToday', views.nbr_cmd_today, name='getNbrCmdToday'),
    path('userInteractions', views.user_interactions, name='userInteractions'),
    path('statistiques/getNbrNewVisitors', views.nbr_new_visitors, name='getNbrNewVisitors'),
    path('ipAddress', views.ip_visitors, name='ipAddress'),
    path('statistiques/getPourcentageClientsGroupes', views.pourcentage_clients_groupes, name='getPourcentageClientsGroupes'),
    path('statistiques/getCmdByRegion/<str:start_date>/<str:end_date>', views.get_cmd_regions),
]
