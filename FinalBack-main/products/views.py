import os
import psycopg2
from django.db.models import Count, Min, Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import views, renderers
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from panier.models import ProductProduct, ProductAvailability, ProductAttributes
from partners.models import Company
from products.models import ProductUOM, ProductTemplate, ProductCategory, ProductPackaging, ProductFinal, Parametres
from products.serializers import ProductSerializer, ProductCategorySerializer, ProductFinalSerializer, \
    CompanySerializer, ParametresSerializer

connect= psycopg2.connect(user="postgres",
                              password="limil1000",
                              host="localhost",
                              port="5432",
                              database="dbtest")
cursortest = connect.cursor()
connect.autocommit=True
'''
connect= psycopg2.connect(user="student",
                              password="StudenT!",
                              host="10.20.10.101",
                              port="5432",
                              database="hasnaoui20221108")
cursortest = connect.cursor()
connect.autocommit=True
'''
#JOBS ---------------------------------------------
def importProductAvilabilityJob():
    try:
        #ProductAvailability.objects.all().delete()
        '''cursortest.execute('SELECT * FROM public.student_esi_products_puma_availability')
        data = cursortest.fetchall()
        for row in data:
            try:
                prod = ProductProduct.objects.get(id=row[2])
                available = ProductAvailability(state=row[0], default_code=row[1], product_id=prod, name_template=row[3], product_category=row[4], qty=row[5], location_id=row[6], location_name=row[7], unit=row[8])
                available.save()
            except Exception as e:
                print(e)
                break'''
        print('new')
        return HttpResponse("Import product availability done.")
    except Exception as e:
        print(e)

def importProductAttributesJob():
    '''existing_ids = list(ProductAttributes.objects.values_list('id', flat=True))
    cursortest.execute('SELECT * FROM public.student_esi_product_puma_product_attributes where id NOT IN %s', (tuple(existing_ids),))
    data = cursortest.fetchall()
    if(len(data)>0):
        for row in data:
            try:
                prod = ProductProduct.objects.get(id=row[0])
                attr = ProductAttributes(
                    id=row[2],
                    product_id=prod,
                    default_code=row[1],
                    product_attribute_id=row[5],
                    product_attribute=row[6],
                    product_attribute_value_id=row[3],
                    product_attribute_value=row[4],
                )
                attr.save()
            except Exception as e:
                print(e)'''
    print('neww')
    return HttpResponse("Import new product attributes done.")

def importProductProductJob():
    existing_ids = list(ProductProduct.objects.values_list('id', flat=True))
    cursortest.execute('SELECT id, product_tmpl_id, default_code, ean13, code_wavesoft FROM public.product_product where id NOT IN %s', (tuple(existing_ids),))
    data = cursortest.fetchall()
    if(len(data)>0):
        for row in data:
            try:
                prod = ProductTemplate.objects.filter(id=row[1]).first()
                productp = ProductProduct(id=row[0], product_tmpl_id= prod,  default_code=row[2], ean13=row[3], code_wavesoft=row[4])
                productp.save()
            except Exception as e:
                print(e)
    return HttpResponse("Import new product product done.")

def importProductPackagingJob():
    existing_ids = list(ProductPackaging.objects.values_list('id', flat=True))
    cursortest.execute('SELECT id, product_tmpl_id, ul_name, qty  FROM public.product_packaging WHERE  id NOT IN %s', (tuple(existing_ids),))
    data = cursortest.fetchall()
    if(len(data)>0):
        for row in data:
            try:
                prod = ProductTemplate.objects.filter(id=row[1])
                for p in prod:
                    productpackaging = ProductPackaging(id=row[0], product_tmpl_id=p, ul_name=row[2], qty=row[3])
                    productpackaging.save()
            except Exception as e:
                print(e)
    return HttpResponse("Import new productPackaging done.")

def importProductTemplateJob():
    existing_ids = list(ProductTemplate.objects.values_list('id', flat=True))
    cursortest.execute("SELECT * FROM public.product_template WHERE company_id=8 AND sale_ok=True AND id NOT IN %s", (tuple(existing_ids),))
    data = cursortest.fetchall()
    if len(data)>0:
        for row in data:
            uom = ProductUOM.objects.filter(id=row[9]).first()
            categ = ProductCategory.objects.filter(id=row[15]).first()
            company = Company.objects.filter(id = row[18]).first()
            try:
                product = ProductTemplate( id=row[0], warranty=row[1], uos_id=row[2], list_price=row[3], weight=row[4], color=row[5], image=row[6], write_uid=row[7], mes_type=row[8],uom_id=uom,  description_purchase=row[10],
                    create_date=row[11], uos_coeff=row[12], create_uid=row[13], sale_ok=row[14], categ_id=categ, product_manager=row[16], message_last_post=row[17],  company_id= company, state=row[19], uom_po_id=row[20],
                    description_sale=row[21],  description=row[22], weight_net=row[23], volume=row[24], write_date=row[25], active=row[26],  rental=row[27], image_medium=row[28], name=row[29], type=row[30],
                    image_small=row[31], sale_delay=row[32], is_kit=row[33], is_system=row[34], can_be_sold_without_kit=row[35], accept_supplements=row[36], min_price_variant=row[37], template_code=row[38], accept_variant=row[39],
                    loc_rack=row[40], track_all=row[41], loc_row=row[42], loc_case=row[43], track_incoming=row[44], track_outgoing=row[45], stock_method=row[46], purchase_ok=row[47], use_time=row[48], life_time=row[49],
                    removal_time=row[50], alert_time=row[51], track_production=row[52], produce_delay=row[53], use_serial_number=row[54], manage_by_surface_or_volume=row[55], prefix_38_imp=row[56], prefix_category=row[57], prefix_3=row[58], prefix_38_inter=row[59],
                    prefix_6_expense=row[60], prefix_ff=row[61], prefix_38=row[62], prefix_gf=row[63], prefix_6_variation=row[64], prefix_7_income=row[65], prefix_38_local=row[66], prefix_al=row[67], prefix_7_production=row[68], gmao_service=row[69]
                )
                product.save()
            except Exception as e:
                print(e)
    return HttpResponse("Import new product template done.")

#---------------------------------------------------

def importProductAvilability(request):
    cursortest.execute('''select *, CASE
                          WHEN strpos(location_name, '(') > 0 AND strpos(location_name, ')') > 0
                          THEN SUBSTRING(
                            location_name,
                            strpos(location_name, '(') + 1,
                            strpos(location_name, ')') - strpos(location_name, '(') - 1
                          )
                          ELSE ''
                        END AS depot_name
                      FROM public.student_esi_products_puma_availability''')
    data = cursortest.fetchall()
    for row in data:
        try:
            prod = ProductProduct.objects.get(id=row[2])
            available = ProductAvailability(state=row[0], default_code = row[1], product_id = prod, name_template =row[3],product_category  = row[4],qty =  row[5],location_id =  row[6],location_name =  row[7],unit =  row[8],depot_name =  row[9])
            available.save()
        except Exception as e:
            print(e)
    return HttpResponse("Import product availability done.")
def importProductAttributes(request):
    cursortest.execute('SELECT * FROM public.student_esi_product_puma_product_attributes')
    data = cursortest.fetchall()


    for row in data:
        try:

            prod = ProductProduct.objects.get(id =  row[0] )
            attr = ProductAttributes(product_id =prod,default_code = row[1], product_attribute_id = row[5],product_attribute = row[6],product_attribute_value_id = row[3],product_attribute_value = row[4],)
            attr.save()
        except Exception as e:
            print(e)

    return HttpResponse("Import product attributes done.")



@api_view(['GET'])
def getPaginatedProducts(request):
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')

    offset = int(offset) if offset else 0
    limit = int(limit) if limit else 10

    sql_query = f"select s.qty , p.\"name\" , p.image, p.list_price , c.\"name\" from product_template p left join product_product pp on pp.product_tmpl_id = p.id left join stock_quant s on s.product_id = pp.id left join product_category c on c.id = p.categ_id where p.company_id = 8 and p.list_price != 0 and s.qty is not null order by p.id  OFFSET {offset} LIMIT {limit}"

    cursortest.execute(sql_query)
    results = cursortest.fetchall()
    return JsonResponse(results, safe=False)

def importProductProduct(request):
    cursortest.execute('SELECT id, product_tmpl_id, default_code, ean13, code_wavesoft, lst_price FROM public.product_product')
    data = cursortest.fetchall()
    for row in data:
        prod = ProductTemplate.objects.filter(id = row[1]).first()
        productp = ProductProduct(id=row[0], product_tmpl_id= prod,  default_code=row[2], ean13=row[3], code_wavesoft=row[4], lst_price=row[5])
        productp.save()
    return HttpResponse("Import product product done.")

def importProductUOM(request):
    cursortest.execute('SELECT id, name, rounding, factor, uom_type FROM public.product_uom')
    data = cursortest.fetchall()
    for row in data:
        productUOM = ProductUOM(id=row[0], name=row[1],  rounding=row[2],  factor =row[3], uom_type=row[4])
        productUOM.save()
    return HttpResponse("Import productUOM done.")
def importCompany(request):
    cursortest.execute('SELECT  id, "name" FROM public.res_company')
    data = cursortest.fetchall()
    for row in data:
        try:
            company = Company(id=row[0], name=row[1])
            company.save()
        except Exception as e:
            print(f"Error: {e}")
    return HttpResponse("Import comapny done.")

def importProductPackaging(request):
    cursortest.execute('SELECT id, product_tmpl_id, ul_name, qty  FROM public.product_packaging')
    data = cursortest.fetchall()
    print(len(data))
    for row in data:
        prod = ProductTemplate.objects.filter(id=row[1])
        for p in prod:
            productpackaging = ProductPackaging(id=row[0], product_tmpl_id=p, ul_name=row[2], qty=row[3])
            productpackaging.save()
    return HttpResponse("Import productPackaging done.")
def importProductCategory(request):
    cursortest.execute('select id, "name", company_id from product_category  where company_id=8 or company_id is null group by ("name", id)')
    data = cursortest.fetchall()
    for row in data:
        product_category = ProductCategory(id=row[0], name=row[1], company_id=row[2])
        product_category.save()
    return HttpResponse("Import Categorie done.")
def importProductTemplate(request):
    print('Ok1')
    cursortest.execute('SELECT * FROM public.product_template where company_id=8 and sale_ok=True')
    data = cursortest.fetchall()
    print('Ok')
    for row in data:
        uom = ProductUOM.objects.filter(id=row[9]).first()
        categ = ProductCategory.objects.filter(id=row[15]).first()
        company = Company.objects.filter(id = row[18]).first()

        try:
            product = ProductTemplate( id=row[0], warranty=row[1], uos_id=row[2], list_price=row[3], weight=row[4], color=row[5], image=row[6], write_uid=row[7], mes_type=row[8],uom_id=uom,  description_purchase=row[10],
                create_date=row[11], uos_coeff=row[12], create_uid=row[13], sale_ok=row[14], categ_id=categ, product_manager=row[16], message_last_post=row[17],  company_id= company, state=row[19], uom_po_id=row[20],
                description_sale=row[21],  description=row[22], weight_net=row[23], volume=row[24], write_date=row[25], active=row[26],  rental=row[27], image_medium=row[28], name=row[29], type=row[30],
                image_small=row[31], sale_delay=row[32], is_kit=row[33], is_system=row[34], can_be_sold_without_kit=row[35], accept_supplements=row[36], min_price_variant=row[37], template_code=row[38], accept_variant=row[39],
                loc_rack=row[40], track_all=row[41], loc_row=row[42], loc_case=row[43], track_incoming=row[44], track_outgoing=row[45], stock_method=row[46], purchase_ok=row[47], use_time=row[48], life_time=row[49],
                removal_time=row[50], alert_time=row[51], track_production=row[52], produce_delay=row[53], use_serial_number=row[54], manage_by_surface_or_volume=row[55], prefix_38_imp=row[56], prefix_category=row[57], prefix_3=row[58], prefix_38_inter=row[59],
                prefix_6_expense=row[60], prefix_ff=row[61], prefix_38=row[62], prefix_gf=row[63], prefix_6_variation=row[64], prefix_7_income=row[65], prefix_38_local=row[66], prefix_al=row[67], prefix_7_production=row[68], gmao_service=row[69]
            )
        except Exception as e:
            print(e)
        product.save()
    return HttpResponse("Import product done.")



def safe_open_w(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'wb')
@api_view(['GET'])
def getProducts(request):
    products = ProductTemplate.objects.filter( description__isnull=False)
    serializers = ProductSerializer(products, many=True)
    product_data = serializers.data
    '''for i, product in enumerate(products):
        try:
            prod = ProductPackaging.objects.filter(product_tmpl_id=product.id).first()
            if prod:
                qty = prod.qty
            else:
                qty = 1
        except Exception as e:
            print(e, product.id)
        product_data[i]['qty_cond'] = qty'''
    return Response(product_data)


@api_view(['GET'])
def getProductById(request, product_id):
    try:
        product = ProductTemplate.objects.get(id=product_id)
        variantes = ProductFinal.objects.filter(tmpl_id = product_id)
        serializer = ProductSerializer(product)
        serialized_data = serializer.data
        produit = ProductPackaging.objects.filter(product_tmpl_id=product_id).first()

        if produit:
            serialized_data['qty_cond']  = produit.qty
        else:
           serialized_data['qty_cond']  = 1
        category=product.categ_id
        serialized_data['category'] = category.name
        if(product.accept_variant):
            variants_data = []
            for variante in variantes:
                prod = ProductProduct.objects.get(id=variante.product_product_id)
                variant_data = {
                    'prod_price': prod.lst_price,
                    'prod_id':variante.product_product_id,
                    'tmpl_id': product_id,
                    'attribute': variante.attribute,
                    'attribute_value': variante.attribute_value
                }
                variants_data.append(variant_data)
            serialized_data['variants'] = variants_data
        else:
            try:
                prod = ProductProduct.objects.filter(product_tmpl_id=product_id).first()
                serialized_data['prod_price'] = prod.lst_price
            except Exception as e:
                print(e)

        return Response(serialized_data)
    except ProductTemplate.DoesNotExist:
        raise NotFound()

@api_view(['GET'])
def GetAndAddFinalToCart(request, product_id, product_product_id):
    try:
        variantes = ProductFinal.objects.filter(tmpl_id=product_id, product_product_id= product_product_id)
        attribute= []
        for variant in variantes:
            attribute.append({'attribute':variant.attribute, 'value': variant.attribute_value})
        prod_p = ProductProduct.objects.get(id=product_product_id)
        if variantes:
            serializer = ProductFinalSerializer(variantes.first())
            product_data = serializer.data
            prod = ProductPackaging.objects.filter(product_tmpl_id=product_id).first()
            if prod:
                qty = prod.qty
            else:
                qty = 1
            '''NOT SURE ABOUT THIS'''
            for v in variantes:
                if v.attribute == 'Poids':
                    qty = float(v.attribute_value.split(' ')[0])
                    print(qty)
            '''NOT SURE ABOUT THIS'''


            product_data['qty_cond'] = qty
            product_data['prod_price'] = prod_p.lst_price
            product_data['variantes_choice'] = attribute

            return Response(product_data)
    except ProductTemplate.DoesNotExist:
        raise NotFound()


@api_view(['GET'])
def getMinMaxPrice(request):
    min_price = ProductTemplate.objects.aggregate(min_price=Min('list_price')).get('min_price')
    max_price = ProductTemplate.objects.aggregate(max_price=Max('list_price')).get('max_price')
    response_data = {
        'min_price': min_price,
        'max_price': max_price
    }
    return Response(response_data)


@api_view(['GET'])
def getProductByName(request):
    search_query = request.GET.get('q', '')
    products = ProductTemplate.objects.filter(company_id=8, sale_ok=True, name__icontains=search_query)
    if not products:
        return Response([])
    if not search_query:
        return Response([])
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCategory(request):
    search_query = request.GET.get('q', '')
    categories = ProductCategory.objects.annotate(num_products=Count('producttemplate')).filter(num_products__gte=1,
                                                                                                name__icontains=search_query)
    if not categories:
        return Response([])
    serializer = ProductCategorySerializer(categories, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def filterByPrice(request, min_price, max_price):
    product = ProductTemplate.objects.filter(list_price__range=(min_price, max_price))
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def filterByPrice(request, min_price, max_price):
    product = ProductTemplate.objects.filter(list_price__range=(min_price, max_price))
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)
class getProductsByCateg(views.APIView):
    renderer_classes = [renderers.JSONRenderer]
    def get(self, request, category_id):
        product = get_object_or_404(ProductCategory, id=category_id)
        products = ProductTemplate.objects.filter(categ_id=product, company_id=8)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
@api_view(['GET'])
def filterCombine(request, categ_id, min_price, max_price):
    if categ_id is not None and  categ_id != 'undefined':
        categ = ProductCategory.objects.filter(id = int(categ_id)).first()
        product = ProductTemplate.objects.filter(list_price__range=(min_price, max_price), categ_id= categ)
    else:
        product = ProductTemplate.objects.filter(list_price__range=(min_price, max_price))
    serializer = ProductSerializer(product, many=True)
    print(len(serializer.data))
    return Response(serializer.data)
class ProductCategoryView(views.APIView):
    renderer_classes = [renderers.JSONRenderer]
    def get(self, request):
        categories = ProductCategory.objects.annotate(num_products=Count('producttemplate')).filter(num_products__gte=1)
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def disponibleEnStock(request):
    cursortest.execute('''select pp.*, pa.qty from products_producttemplate pp 
                            left join panier_productproduct pp2 on pp2.product_tmpl_id_id = pp.id  
                            left join panier_productavailability pa on pa.id = pp2.id
                            where pp.list_price != 0 and image is not null and pp.accept_variant = false   and   pa.qty is not null and pa.qty >0
                        ''')
    data = cursortest.fetchall()
    finalArray = []
    try:
        for row in data:
            product = ProductTemplate.objects.get(id= row[0])
            serializer = ProductSerializer(product).data
            finalArray.append({'product': serializer, 'qty': row[70]})

    except Exception as e:
        print(e)
    return Response(finalArray)


@api_view(['GET'])
def getImages(request):
    '''filenames = next(os.walk(image_path), (None, None, []))[2]
        exclure = ""
        for nom in filenames:
            exclure = exclure+"'"+nom[:-4]+"'"+","
        l = len(exclure)
        exclure = exclure[:l-1]
        condition = ""
        if len(exclure)>0:
            condition = ""
        else:'''
    image_path = "E:\ReactProjects\FrontMyPart-main\src\client\Assets\images\products"
    photos = ProductTemplate.objects.values_list('image', 'id')
    for photo in photos:
        image, id = photo
        try:
           ''' if image is not None:
                image = image.tobytes()
                with open(f"{image_path}\{id}.png", "wb") as output_file:
                    output_file.write(base64.decodebytes(image))'''
           if image is None:
               default_image_path = "E:\ReactProjects\FrontMyPart-main\src\client\Assets\images\products\slider1.png"
               with open(default_image_path, "rb") as default_file:
                   default_image = default_file.read()
               with open(os.path.join(image_path, f"{id}.png"), "wb") as output_file:
                   output_file.write(default_image)
        except Exception as e:
            print(f"Error: {e}")
    return HttpResponse('Ok')


def addtempl(request):

    cursortest.execute('''SELECT  pt.*, pp.id as product_product_id, pa.product_attribute , pa.product_attribute_value 
                            FROM public.products_producttemplate pt
                            left join public.panier_productproduct pp  on pt.id = pp.product_tmpl_id_id
                            left join public.panier_productattributes pa on pa.product_id_id = pp .id
                            WHERE pt.id IN (
                              SELECT pp.product_tmpl_id_id
                              FROM public.panier_productproduct pp
                              LEFT JOIN public.panier_productattributes pa ON pa.product_id_id = pp.id
                            )
                            ''')
    data = cursortest.fetchall()
    print('-----------------------------')

    for p in data:
        try:
            uom = ProductUOM.objects.filter(id=p[69]).first()
            categ = ProductCategory.objects.filter(id=p[67]).first()
            company = Company.objects.filter(id = p[68]).first()
            product = ProductFinal(
                tmpl_id = p[0],
                warranty=p[1],
                uos_id=p[2],
                list_price=p[3],
                weight=p[4],
                color=p[5],
                image=p[6],
                mes_type=p[8],
                uom_id=uom,
                description_purchase=p[9],
                sale_ok=p[13],
                categ_id=categ,
                company_id=company,
                state=p[16],
                uom_po_id=p[17],
                description_sale=p[18],
                description=p[19],
                weight_net=p[20],
                volume=p[21],
                active=p[23],
                name=p[26],
                type=p[27],
                sale_delay=p[29],
                is_kit=p[30],
                is_system=p[31],
                can_be_sold_without_kit=p[32],
                accept_supplements=p[33],
                min_price_variant=p[34],
                template_code=p[35],
                accept_variant=p[36],
                track_all=p[38],
                track_incoming=p[41],
                track_outgoing=p[42],
                stock_method=p[42],
                purchase_ok=p[44],
                track_production=p[49],
                produce_delay=p[50],
                use_serial_number=p[51],
                manage_by_surface_or_volume=p[52],
                product_product_id=p[70],
                attribute=p[71],
                attribute_value=p[72],
            )
            product.save()
            print('--------------------------------------')
        except Exception as e:
            print(e)
            break;

    return HttpResponse('Ok')

@api_view(['GET'])
def getFialiales(request):
    data = Company.objects.order_by('name')
    data_serialized = CompanySerializer(data, many=True)
    return Response(data_serialized.data)

@api_view(['GET'])
def getSettings(request):
    data = Parametres.objects.first()
    data_serialized = ParametresSerializer(data)
    return Response(data_serialized.data)

@api_view(['PATCH'])
def editSettings(request):
    settings = Parametres.objects.first()
    try:
        if request.data.get('company_name') is not None and request.data['company_name'].strip() != '':
            settings.company_name = request.data.get('company_name')
        if request.data.get('tva') is not None and request.data['tva'].strip() != '':
            settings.tva = request.data.get('tva')
    except Exception as e:
        print(e)
    settings.save()
    return Response({'id': settings.id})