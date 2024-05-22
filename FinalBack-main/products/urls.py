from . import views
from django.urls import path, re_path

from .views import GetAndAddFinalToCart, getMinMaxPrice, disponibleEnStock, getFialiales, getSettings

urlpatterns = [
    path('importavailability', views.importProductAvilability),
    path('importattributes', views.importProductAttributes),
    path('importproductuom', views.importProductUOM),
    path('importcompany', views.importCompany),
    path('importproductcategory', views.importProductCategory),
    path('importproducts', views.importProductTemplate),
    path('importproductpackaging', views.importProductPackaging),
    path('importproductproduct', views.importProductProduct),
    path('importavailability', views.importProductAvilability),
    path('importattributes', views.importProductAttributes),
    path('getallproducts', views.addtempl),
    path('getproducts', views.getProducts),
    path('getimages', views.getImages),
    path('getproductsPaginate', views.getPaginatedProducts),
    path('getCategory', views.ProductCategoryView.as_view(), name='categories'),
    path('getproductsByCategory/<int:category_id>', views.getProductsByCateg.as_view()),
    path('getproduct/<int:product_id>/', views.getProductById),
    path('getproductsQuery', views.getProductByName, name='getProductByName'),
    path('getCatgQuery', views.getCategory, name='getProductByName'),
    path('importproductproduct', views.importProductProduct, name='getProductPoduct'),
    path('filterprice/<int:min_price>/<int:max_price>/',views.filterByPrice, name="filterByPrice"),
    path('filtercombine/<str:categ_id>/<int:min_price>/<int:max_price>/',views.filterCombine, name="filterByPrice"),
    path('getfinalbyid/<int:product_id>/<int:product_product_id>/', GetAndAddFinalToCart),
    path('getminmaxprice/', getMinMaxPrice),
    path('getdisponible/', disponibleEnStock),
    path('getcompanies/', getFialiales),
    path('getsettings/', getSettings),
    path('editSettings/', views.editSettings),
    # Other URL patterns
]