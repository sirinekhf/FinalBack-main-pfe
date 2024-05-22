from datetime import timedelta, datetime

import pandas as pd
import psycopg2
from django.http import HttpResponse, JsonResponse
from mlxtend.preprocessing import TransactionEncoder
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from sklearn.preprocessing import StandardScaler

from ML.models import FrequentItemset, UserInteraction, Visitor
from products.models import ProductTemplate, ProductFinal, ProductCategory
from products.serializers import ProductSerializer, ProductCategorySerializer

connect= psycopg2.connect(user="postgres",
                              password="limil1000",
                              host="localhost",
                              port="5432",
                              database="dbtest")
cursor = connect.cursor()
connect.autocommit=True

@api_view(['GET'])
def get_cmd_regions(request, start_date, end_date):

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    try:

        start_date2 = datetime.strptime(start_date, "%d-%m-%Y")

        end_date2 = datetime.strptime(end_date, "%d-%m-%Y")
        num_days = (end_date2 - start_date2).days
    except Exception as e:
        print(e)


    cursor.execute(
        """
        SELECT pr.region, DATE(ps.create_date), COUNT(ps.id)
        FROM partners_rescountrystate pr
        INNER JOIN public.partners_partners pp ON pr.id = pp.state_id_id
        INNER JOIN public.panier_saleorder ps ON pp.id = ps.partner_id_id
        WHERE ps.create_date BETWEEN %s AND %s
        GROUP BY pr.region, DATE(ps.create_date)
        """,
        [start_date, end_date],
    )
    result1 = cursor.fetchall()
    regions_names = []
    for row in result1:
        region = row[0]
        if region not in regions_names:
            regions_names.append(region)



    final_array = []
    for region in regions_names:
        result_array = []
        for i in range(num_days + 1):
            current_date = start_date2 + timedelta(days=i)
            result_array.append({"x": current_date.strftime("%d"), "y": 0})

        for row in result1:
            if region == row[0]:
                try:
                    date_index = (datetime.strptime(str(row[1]), "%Y-%m-%d") -  start_date2).days
                except Exception as e:
                    print(e)

                result_array[date_index]["y"] = row[2]
                
        final_array.append({"id": region, "data": result_array})

    return Response(final_array)
'''@api_view(['GET'])
def get_cmd_regions(request, start_date, end_date):
    if (start_date > end_date):
        temp = start_date
        start_date = end_date
        end_date = temp
    cursor.execute("""SELECT pr.region,  COUNT(ps.id), pp3."name"  AS number_of_saleorders
        FROM partners_rescountrystate pr 
        INNER JOIN public.partners_partners pp ON pr.id = pp.state_id_id 
        INNER JOIN public.panier_saleorder ps ON pp.id = ps.partner_id_id 
        INNER JOIN public.panier_saleorderline ps2 ON ps.id = ps2.order_id_id 
        INNER JOIN public.panier_productproduct pp2 ON ps2.product_id_id  = pp2.id
        INNER JOIN public.products_producttemplate tp ON pp2.product_tmpl_id_id = tp.id
        INNER JOIN public.products_productcategory t ON tp.categ_id_id = t.id 
        inner join public.products_productcategory pp3 on pp3.id = t.id 
        where ps.create_date between %s and %s
        GROUP BY pr.region , pp3."name" """, [start_date, end_date])
    result1 = cursor.fetchall()
    regions_names =[]
    categories=[]
    for row in result1:
        region =row[0]
        if row[2] not in categories:
            categories.append(row[2])

        if region not in regions_names:
            regions_names.append(region)
    final_array = []
    for region in regions_names:
        result_array =[]
        for row in result1:
            if region == row[0]:
                result_array.append({'x':row[2], 'y':row[1]})
        regions_categories=[]
        for row in result_array:
            regions_categories.append(row['x'])
        for cat in categories:
            if cat not in regions_categories:
                result_array.append({'x': cat, 'y':0})
        sorted_result = sorted(result_array, key=lambda item: item['x'])
        final_array.append({
            'id': region,
            'data': sorted_result
        })

    return Response(final_array)'''


@api_view(['GET'])
def pourcentage_clients_groupes(request):
    with connect.cursor() as cursor:
        query1 = """
            SELECT count(*) AS nb_groupes
            FROM users_user uu 
            WHERE uu.is_client_groupe = True ;
        """
        cursor.execute(query1)
        result1 = cursor.fetchone()

        query2 = """ SELECT count(*) AS nb_groupes FROM users_user uu ;"""
        cursor.execute(query2)
        result2 = cursor.fetchone()
        nbr_clients_groupes = result1[0]
        nbr_clients_all = result2[0]
        if (nbr_clients_groupes == 0 and nbr_clients_all == 0):
            pourcentage_groupes = 0
        else:
            pourcentage_groupes = (nbr_clients_groupes * 100) / nbr_clients_all
    return Response(pourcentage_groupes)

@api_view(['GET'])
def ip_visitors(request):
    ip_address = request.META.get('REMOTE_ADDR')
    v = Visitor.objects.filter(ip_address=ip_address).first()
    if v not in Visitor.objects.all():
        visitor = Visitor(ip_address=ip_address)
        visitor.save()
    return Response('Hello visitor')

class user_interactions(APIView):
    def post(self, request):
        user = request.data.get('user')
        product_id = request.data.get('productId')
        action_type = request.data.get('actionType')
        user_interaction = UserInteraction(user=user, product_id=product_id, action_type=action_type)
        user_interaction.save()
        return Response(' interaction saved ')

@api_view(['GET'])
def nbr_new_visitors(request):

    with connect.cursor() as cursor:
        query = """
            SELECT COUNT(*) AS nb_v
            FROM "ML_visitor" mv
        """

        cursor.execute(query)
        result = cursor.fetchone()

        nbr_new_visitors = result[0]
    return Response(nbr_new_visitors)

def handle_user_interactions(request):
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM public.ML_userinteraction")
        user_interaction_data = cursor.fetchall()
    column_names = ['column1', 'column2', 'column3']  # Replace with the actual column names in your table
    user_interaction_data = pd.DataFrame(user_interaction_data, columns=column_names)
    #user_interaction_data = user_interaction_data.drop(['irrelevant_column'], axis=1)

    # missing values
    user_interaction_data = user_interaction_data.dropna()

    # Transform the data
    # Apply one-hot encoding or label encoding for categorical variables
    user_interaction_data = pd.get_dummies(user_interaction_data, columns=['categorical_variable'])

    # Normalize numerical variables
    scaler = StandardScaler()
    numerical_variables = ['numerical_variable1', 'numerical_variable2']
    user_interaction_data[numerical_variables] = scaler.fit_transform(user_interaction_data[numerical_variables])

    # Perform further preprocessing or feature engineering as required
    cursor.close()


@api_view(['GET'])
def nbr_cmd_today(request):
    with connect.cursor() as cursor:
        query1 = """
                    SELECT count(*) AS nb_cmd
                    FROM public.panier_saleorder ps 
                    WHERE DATE(ps.create_date) = CURRENT_DATE
                    
                """
        cursor.execute(query1)
        result1 = cursor.fetchone()

        query2 = """
                     SELECT count(*) AS nb_cmd
                    FROM public.panier_saleorder ps 
                    WHERE DATE(ps.create_date) = CURRENT_DATE - INTERVAL '1 day'
                    
                        """
        cursor.execute(query2)
        result2 = cursor.fetchone()

    nbr_cmd_today = result1[0]
    nbr_cmd_yesterday = result2[0]
    difference = nbr_cmd_today - nbr_cmd_yesterday
    if( nbr_cmd_yesterday == 0 and nbr_cmd_today == 0):
        progress = 0
    else:
        if (nbr_cmd_yesterday == 0):
            progress = 1
        else:
            progress = (difference / nbr_cmd_yesterday)

    stat_cmds = []
    stat_cmds.append({
        'nbr_cmd_today': nbr_cmd_today,
        'nbr_cmd_yesterday': nbr_cmd_yesterday,
        'progress': progress
    })
    #data = {'nbr_cmd_today': nbr_cmd_today}
    return Response(stat_cmds)

@api_view(['GET'])
def total_revenue_today(request):
    with connect.cursor() as cursor:
        query1 = """
                    SELECT SUM(amount_total) AS total_sales
                    FROM public.panier_saleorder ps 
                    WHERE DATE(ps.write_date) = CURRENT_DATE
                    AND state = 'paid';
                """
        cursor.execute(query1)
        result1 = cursor.fetchone()

        query2 = """SELECT SUM(amount_total) AS total_sales
                    FROM public.panier_saleorder ps
                    WHERE DATE(ps.write_date) = CURRENT_DATE - INTERVAL '1 day'
                    AND state = 'paid';
                """
        cursor.execute(query2)
        result2 = cursor.fetchone()

    total_revenue_today = result1[0]
    total_revenue_yesterday = result2[0]
    if total_revenue_yesterday is None:
        total_revenue_yesterday=0
    if total_revenue_today is None:
        total_revenue_today=0


    difference = total_revenue_today - total_revenue_yesterday

    if (total_revenue_yesterday == 0 and total_revenue_today == 0):
        progress = 0
    else:
        if (total_revenue_yesterday == 0):
            progress = 1
        else:
            progress = (difference / total_revenue_yesterday)

    stat_revenue = []
    stat_revenue.append({
        'total_revenue_today': total_revenue_today,
        'total_revenue_yesterday': total_revenue_yesterday,
        'progress': progress
    })

    return Response(stat_revenue)

@api_view(['GET'])
def nbr_new_clients_week(request):
    with connect.cursor() as cursor:
        query = """
            SELECT COUNT(*) AS new_clients_count
            FROM users_user uu 
            WHERE EXTRACT(YEAR FROM uu.date_joined) = EXTRACT(YEAR FROM CURRENT_DATE)
            AND EXTRACT(WEEK FROM uu.date_joined) = EXTRACT(WEEK FROM CURRENT_DATE)
            AND uu.is_comercial=FALSE and uu.is_admin=FALSE;
        """
        cursor.execute(query)
        result1 = cursor.fetchone()

        query2 = """
                    SELECT COUNT(*) AS new_clients_count
                    FROM users_user uu 
                    WHERE EXTRACT(YEAR FROM uu.date_joined) = EXTRACT(YEAR FROM CURRENT_DATE)
                    AND EXTRACT(WEEK FROM uu.date_joined) = EXTRACT(WEEK FROM CURRENT_DATE) - 1
                    AND uu.is_comercial=FALSE and uu.is_admin=FALSE;
                """
        cursor.execute(query2)
        result2 = cursor.fetchone()
        nbr_new_clients_this_week = result1[0]
        nbr_new_clients_last_week = result2[0]

        difference = nbr_new_clients_this_week - nbr_new_clients_last_week

        if (nbr_new_clients_last_week == 0 and nbr_new_clients_this_week == 0):
            progress = 0
        else:
            if (nbr_new_clients_last_week == 0):
                progress = 1
            else:
                progress = (difference / nbr_new_clients_last_week)
    stat_clients = []
    stat_clients.append({
        'nbr_new_clients_this_week': nbr_new_clients_this_week,
        'nbr_new_clients_last_week': nbr_new_clients_last_week,
        'progress': progress
    })
    #data = {'nbr_new_clients_week': nbr_new_clients_week}
    return Response(stat_clients)

@api_view(['GET'])
def get_top_categories(request, start_date, end_date):
    sql_query = '''
          SELECT pt.categ_id_id, pp2."name" , SUM(ps.price_unit* ps.product_uos_qty ) AS total_amount
        FROM public.panier_saleorderline ps 
        JOIN public.panier_productproduct pp ON ps.product_id_id = pp.id 
        JOIN public.products_producttemplate pt ON pp.product_tmpl_id_id = pt.id
        JOIN public.products_productcategory pp2 on pp2.id = pt.categ_id_id
        WHERE ps.create_date BETWEEN %s AND %s
        group by pt.categ_id_id , pp2."name" 
        ORDER BY total_amount DESC
        LIMIT 10;
    '''
    if(start_date > end_date):
        temp = start_date
        start_date = end_date
        end_date = temp

    with connect.cursor() as cursor:
        cursor.execute(sql_query, [start_date, end_date])
        results = cursor.fetchall()

    chiffres_affaires = []
    category_ids = []
    for row in results:
        chiffres_affaires.append({
            'category_id': row[0],
            'category_name': row[1],
            'total_CA': row[2]
        })
        category_ids.append(row[0])
    return Response(chiffres_affaires)
@api_view(['GET'])
def get_top_products(request, start_date, end_date):
    sql_query = '''SELECT "ML_vente"."produit_id", SUM("ML_vente"."montant") AS "total"
        FROM public."ML_vente"
        WHERE "ML_vente"."date" BETWEEN %s AND %s
        GROUP BY "ML_vente"."produit_id"
        ORDER BY total DESC
        LIMIT 10;
    '''

    with connect.cursor() as cursor:
        cursor.execute(sql_query, [start_date, end_date])
        results = cursor.fetchall()

    chiffres_affaires = []
    produit_ids = []
    for row in results:
        chiffres_affaires.append({
            'product_id': row[0],
            'total_CA': row[1]
        })
        produit_ids.append(row[0])
    try:
        produit_ids = [ca['product_id'] for ca in chiffres_affaires]
        products = ProductTemplate.objects.filter(id__in=produit_ids)
        serializer = ProductSerializer(products, many=True)
    except Exception as e:
        print(f"Error: {e}")


    return Response(chiffres_affaires)

@api_view(['GET'])
def get_top_clients(request, start_date, end_date):
    sql_query = """
        SELECT user_partner_id, SUM(amount_total) AS total_purchase
        FROM public.panier_saleorder
        WHERE create_date BETWEEN %s AND %s
        GROUP BY user_partner_id
        ORDER BY total_purchase DESC
        LIMIT 10;
    """

    with connect.cursor() as cursor:
        cursor.execute(sql_query, [start_date, end_date])
        results = cursor.fetchall()
    top_clients = [{'client_id': row[0], 'total_purchase': row[1]} for row in results]

    return Response(top_clients)


@api_view(['GET'])
def getStatCAbyCategory(request, start_date, end_date):
    sql_query = '''
        SELECT pt.categ_id_id,pp2."name", SUM(ps.price_unit* ps.product_uos_qty ) AS total_amount
        FROM public.panier_saleorderline ps 
        JOIN public.panier_productproduct pp ON ps.product_id_id = pp.id 
        JOIN public.products_producttemplate pt ON pp.product_tmpl_id_id = pt.id
         JOIN public.products_productcategory pp2 ON pt.categ_id_id=pp2.id
        WHERE ps.create_date BETWEEN %s AND %s AND (ps.state='paid' OR ps.state='shipped') 
        GROUP BY pt.categ_id_id, pp2."name" ;
    '''

    with connect.cursor() as cursor:
        cursor.execute(sql_query, [start_date, end_date])
        results = cursor.fetchall()

    chiffres_affaires = []
    category_ids = []
    for row in results:
        chiffres_affaires.append({
            'category_id': row[0],
            'category_name': row[1],
            'total_CA': row[2]
        })
        category_ids.append(row[0])
    try:
        category_ids = [ca['category_id'] for ca in chiffres_affaires]
        categories = ProductCategory.objects.filter(id__in=category_ids)
        serializer = ProductCategorySerializer(categories, many=True)
    except Exception as e:
        print(f"Error: {e}")
    category_data = serializer.data
    #product_data['chiffre affaires'] = [ca['total_CA'] for ca in chiffres_affaires]
    return Response(chiffres_affaires)

@api_view(['GET'])
def getStatCmdbyState(request, start_date, end_date):
    try:
        sql_query = '''
            SELECT state, COUNT(*) AS nb_commandes FROM public.panier_saleorder so
            WHERE so.create_date BETWEEN %s AND %s 
            GROUP BY state '''
        with connect.cursor() as cursor:
            cursor.execute(sql_query, [start_date, end_date])
            results = cursor.fetchall()
    except Exception as e:
        print(e)

    # Process the results
    commandes_par_etat = []
    for row in results:
        etat = row[0]
        nombre_commandes = row[1]
        commandes_par_etat.append({
            'etat': etat,
            'nombre_commandes': nombre_commandes
        })

    return Response(commandes_par_etat)


@api_view(['GET'])
def getStatCAbyProduct(request, start_date, end_date):
    sql_query = '''
        SELECT "ML_vente"."produit_id", SUM("ML_vente"."montant") AS "total"
        FROM public."ML_vente"
        WHERE "ML_vente"."date" BETWEEN %s AND %s
        GROUP BY "ML_vente"."produit_id"
    '''

    with connect.cursor() as cursor:
        cursor.execute(sql_query, [start_date, end_date])
        results = cursor.fetchall()

    chiffres_affaires = []
    produit_ids = []
    for row in results:
        chiffres_affaires.append({
            'product_id': row[0],
            'total_CA': row[1]
        })
        produit_ids.append(row[0])
    try:
        produit_ids = [ca['product_id'] for ca in chiffres_affaires]
        products = ProductTemplate.objects.filter(id__in=produit_ids)
        serializer = ProductSerializer(products, many=True)
    except Exception as e:
        print(f"Error: {e}")
    print(chiffres_affaires)

    return Response(chiffres_affaires)


@api_view(['GET'])
def get_getItemsets(request, product_id):
    frequent_itemsets = pd.read_csv('frequent_itemsets.csv')
    p = get_related_products(frequent_itemsets, product_id)
    product_list = []
    for item in p:
        product = ProductTemplate.objects.filter(id=item).first()
        if product:
            product_list.append(product)
    productt = ProductSerializer(product_list, many=True)
    return Response(productt.data)
def get_related_products(frequent_itemsets, current_selection):
    related_products = set()
    current_selection = frozenset([current_selection])
    for itemset in frequent_itemsets['itemsets']:
        itemset = frozenset(eval(itemset))
        if current_selection.issubset(itemset):
            related_products.update(itemset)
    related_products -= current_selection
    return related_products
