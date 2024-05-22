import psycopg2
from _decimal import Decimal
from django.core.mail import send_mail
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Max

from ML.models import Vente
from panier.Serializers import CommandeSerializer, SaleOrderLineSerializer
from panier.models import SaleOrder, ProductProduct, SaleOrderLine, ProductAvailability
from partners.models import Partners
from products.models import ProductTemplate, ProductPackaging, ProductFinal
from products.serializers import ProductSerializer, ProductFinalSerializer
from users.models import User
from users.serializers import UserSerializer
connect = psycopg2.connect(user="postgres",
                              password="limil1000",
                              host="localhost",
                              port="5432",
                              database="dbtest")
connect.autocommit=True
cursortest = connect.cursor()
'''
connect= psycopg2.connect(user="student", password="StudenT!", host="10.20.10.101", port="5432", database="hasnaoui20221108")
connect.autocommit=True
cursortest = connect.cursor()

@api_view(['GET'])
def importDataToExcel(request):

    try:
        query = 'SELECT subquery.order_id, string_agg(DISTINCT CAST(subquery.product_template_id AS VARCHAR), \', \') AS product_template_ids FROM (SELECT p.order_id, pt.id AS product_template_id FROM public.sale_order_line p JOIN public.product_product pp ON p.product_id = pp.id JOIN public.product_template pt ON pp.product_tmpl_id = pt.id WHERE pt.company_id = 8 AND pt.sale_ok = true AND p.order_id IN ( SELECT order_id FROM ( SELECT order_id, COUNT(DISTINCT pt.id) AS template_count FROM public.sale_order_line p JOIN public.product_product pp ON p.product_id = pp.id JOIN public.product_template pt ON pp.product_tmpl_id = pt.id WHERE pt.company_id = 8 AND pt.sale_ok = true GROUP BY order_id ) AS subquery2 WHERE template_count > 1 )) AS subquery GROUP BY subquery.order_id HAVING COUNT(DISTINCT subquery.product_template_id) > 1 ORDER BY subquery.order_id'
        cursortest.execute(query)
        data = cursortest.fetchall()
        df = pd.DataFrame(data, columns=['order_id', 'product_template_ids'])
        try:
            df.to_excel('output.xlsx', index=False)
            print("Excel file created successfully.")
        except Exception as e:
            print(f"Error creating Excel file: {e}")

    except (psycopg2.Error, pd.errors.PandasError) as e:
        print("Error:", e)
        return HttpResponse({'except is called'})

'''


def sendemail(request, subject, msg, receiver):
    try:
        send_mail(subject, msg, 'raniachahinezabbaci@gmail.com', [receiver], fail_silently=False)
        return render(request, 'sendemail.html')
    except Exception as e:
        return HttpResponseServerError(f"An error occurred while sending the email: {str(e)}")


def createsaleorder(partner, user):
    if partner:
        saleorder = SaleOrder(partner_id=partner, user_partner=user)
        saleorder.save()
        return saleorder
    else:
        return Response({'msg': 'Invalid partner'})


def createsaleorderline(order, order_qty, qty_user, uom, prix, name, state, partner, product, product_packaging):
    try:
        saleorderline = SaleOrderLine(order_id=order,
                                      product_uom_qty=order_qty, product_uos_qty=order_qty, order_uom_qty=order_qty,
                                      qty_conditionnee=qty_user, order_qty_conditionnee=qty_user,
                                      product_uom=uom,
                                      price_unit=prix, name=name, state=state,
                                      order_partner_id=partner, product_id=product, product_packaging=product_packaging)
        saleorderline.save()
        return Response(saleorderline.id)
    except Exception as e:
        print(e)


def updatesaleorderline(saleorderline, state):
    s = saleorderline
    saleorderline.state = state
    s.save()
def updatesaleorderfirst(saleorder_id, untaxed, taxed, total):
    try:
        saleorder = SaleOrder.objects.get(id=saleorder_id.id)
    except SaleOrder.DoesNotExist:
        return Response({'error': 'The sale order line doesn\'t exist'}, status=status.HTTP_404_NOT_FOUND)

    if untaxed is not None:
        saleorder.amount_untaxed = untaxed
    if taxed is not None:
        saleorder.amount_tax = taxed
    if total is not None:
        saleorder.amount_total = total

    saleorder.write_date = timezone.now()

    saleorder.save()
    return Response({'id': saleorder.id})


class updatesaleorderView(APIView):
    def patch(self, request, id, user_id):
        try:

            order = SaleOrder.objects.filter(id=id).first()
            comercial = User.objects.filter(id=user_id).first()
            user = User.objects.filter(id=order.user_partner_id).first()
            email = user.email
            saleorderlines = SaleOrderLine.objects.filter(order_id=id)
        except SaleOrder.DoesNotExist:
            return Response({'error': 'SaleOrder is not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.data.get('state') is not None and request.data['state'].strip() != '':
            if (request.data.get('state') == 'confirm'):
                statee = 'confirmée'
                sendemail(request, 'Hasnaoui Groupe',
                          f'Cher client votre commande est {statee} Veuillez consulter notre site pour effectuer le paiment. Cordialement.',
                          email)
                try:
                    for saleorderline in saleorderlines:
                        updatesaleorderline(saleorderline,'confirm')
                        product = saleorderline.product_id
                        qty = saleorderline.order_uom_qty
                        prix_unitaire = saleorderline.price_unit
                        template = product.product_tmpl_id
                        montant = float(prix_unitaire) * float(qty)
                        vente = Vente(produit = template, quantite=qty, montant=montant, date = timezone.now())
                        vente.save()
                except Exception as e:
                    print(e)
            else:
                if (request.data.get('state') == 'cancel'):
                    statee = 'annulée'
                    try:
                        for saleorderline in saleorderlines:
                            updatesaleorderline(saleorderline, 'cancel')
                    except Exception as e:
                        print(e)
                    if request.data.get('motif') is not None and request.data.get('motif').strip() != '':
                        motif = request.data.get('motif')
                        sendemail(request, 'Hasnaoui Groupe',
                                  f'Cher client votre commande est {statee} Veuillez consulter notre '
                                  f'site pour plus de détails.'
                                  f'Motif:  {motif}.   '
                                  f'Cordialement.', email)
                    else:
                        sendemail(request, 'Hasnaoui Groupe',
                                  f'Cher client votre commande est {statee} Veuillez consulter notre '
                                  f'site pour plus de détails.'
                                  f'Cordialement.', email)
                else:
                    if (request.data.get('state') == 'shipped'):
                        statee = 'en livraison'
                        try:
                            for saleorderline in saleorderlines:
                                updatesaleorderline(saleorderline, 'shipped')
                        except Exception as e:
                            print(e)
                        sendemail(request, 'Hasnaoui Groupe',
                                  f'Cher client votre commande est {statee} Veuillez consulter notre '
                                  f'site pour plus de détails.'
                                  f'Cordialement.', email)
                    else:
                        if (request.data.get('state') == 'paid'):
                            try:
                                for saleorderline in saleorderlines:
                                    updatesaleorderline(saleorderline, 'paid')
                            except Exception as e:
                                print(e)

        order.state = request.data['state']
        order.date_confirm = timezone.now()
        order.date_validite = timezone.now()
        if request.data.get('fiscal_stamp_amount') is not None and request.data['fiscal_stamp_amount'].strip() != '':
            order.fiscal_stamp_amount = Decimal(request.data['fiscal_stamp_amount'])
        if request.data.get('matricule') is not None and request.data['matricule'].strip() != '':
            order.matricule = request.data['matricule']
        if request.data.get('matricule_remorque') is not None and request.data['matricule_remorque'].strip() != '':
            order.matricule_remorque = request.data['matricule_remorque']

        if request.data.get('driver') is not None and request.data['driver'].strip() != '':
            order.driver = request.data['driver']
        if request.data.get('transporter') is not None and request.data['transporter'].strip() != '':
            order.transporter = request.data['transporter']

        if request.data.get('shipped') is not None:
            order.shipped = request.data['shipped']

        if request.data.get('is_contract') is not None:
            order.is_contract = request.data['is_contract']

        if request.data.get('is_convention') is not None:
            order.is_convention = request.data['is_convention']

        order.write_date = timezone.now()
        order.write_uid = comercial

        order.save()
        return Response({"SaleOrder Update success"})


class SubmitOrderView(APIView):
    def post(self, request):
        data = request.data

        cart_items = data.get('cartItems')
        user = data.get('user')
        user_serialized = UserSerializer(user).data
        mail = user_serialized.get('email')
        partner = Partners.objects.filter(email=mail).first()
        user_user = User.objects.filter(email=mail).first()

        if partner:
            saleorder_id = createsaleorder(partner, user_user)
        else:
            return Response({'message': 'Partner does not exist'})

        untaxed = 0
        try:
            for cart_item in cart_items:
                quantity = cart_item.get('qty_cond')
                product = cart_item.get('product')

                try:
                    if (product.get('accept_variant') ):
                        tmpl_id = product.get('tmpl_id')
                        product_id = product.get('product_product_id')
                        product_product = ProductProduct.objects.filter(id=product_id).first()
                        prix_unitaire = product.get('prod_price')
                        attribute = product.get('attribute')
                        attribute_value = product.get('attribute_value')
                    else:
                        tmpl_id = product.get('id')
                        product_product = ProductProduct.objects.filter(product_tmpl_id=tmpl_id).first()
                        prix_unitaire = product_product.lst_price
                    if (prix_unitaire is None):
                        prix_unitaire = 1
                except Exception as e:
                    print(e)
                product_template = ProductTemplate.objects.get(id=tmpl_id)
                name = product_template.name
                prod_uom = product_template.uom_id
                product_packaging = ProductPackaging.objects.filter(product_tmpl_id=tmpl_id).first()
                if product_packaging:
                    if (product.get('accept_variant')):
                        if(attribute != 'Poids'):
                            product_packaging_qty = product_packaging.qty
                        else:
                            product_packaging_qty = 1
                    else:
                        product_packaging_qty = product_packaging.qty
                else:
                    product_packaging_qty = 1
                order_qty = int(quantity) * product_packaging_qty
                untaxed = float(untaxed) + float(prix_unitaire) * float(order_qty)
                createsaleorderline(saleorder_id, order_qty, quantity, prod_uom, prix_unitaire, name, 'draft', partner,product_product, product_packaging)
            taxed = untaxed + untaxed * 0.09
            total = taxed
            updatesaleorderfirst(saleorder_id, untaxed, taxed, total)

        except Exception as e:
            print(e)
        return Response({'OK'})


@api_view(['GET'])
def getAllCommande(requets):
    cmd = SaleOrder.objects.all()
    cmd_serializer = CommandeSerializer(cmd, many=True)
    if not cmd:
        return Response([])
    else:
        return Response(cmd_serializer.data)


@api_view(['GET'])
def getCommandeOfUser(requets, user_email):
    try:
        user = User.objects.filter(email=user_email).first()
        if not user:
            return Response({'user not found'})
        else:
            cmd = SaleOrder.objects.filter(user_partner=user)
            cmd_serializer = CommandeSerializer(cmd, many=True)
            if not cmd:
                return Response([])
            else:
                return Response(cmd_serializer.data)
    except ProductTemplate.DoesNotExist:
        raise NotFound()


@api_view(['GET'])
def getCommandeDetails(request, cmd_id):
    try:
        saleorderline = SaleOrderLine.objects.filter(order_id=cmd_id)
        if not saleorderline:
            return Response([])
        else:
            cmd_serializer = SaleOrderLineSerializer(saleorderline, many=True)
            data = cmd_serializer.data
            try:
                for item in data:
                    product = ProductProduct.objects.filter(id=item['product_id']).first()
                    if product:
                        available = ProductAvailability.objects.filter(product_id =product.id).first()
                        if available:
                            qty_available = ProductAvailability.objects.filter(product_id =item['product_id'])
                            qty = qty_available.aggregate(max_quantity=Max('qty'))['max_quantity']
                            item['qty_available'] = [{'qty': qty.qty, 'name': qty.location_name} for qty in qty_available]
                        else:
                            item['qty_available'] = [{'name':'non disponible',  'qty': ''}]
                            #qty = 0

                        produit = ProductFinal.objects.filter(product_product_id=product.id)
                        attribute = []
                        for variant in produit:
                            attribute.append({'attribute': variant.attribute, 'value': variant.attribute_value})
                        product_data = ProductFinalSerializer(produit.first()).data
                        #product_data['qty_stock'] = qty
                        product_data['price'] = product.lst_price
                        product_data['variantes_choice'] = attribute
                        item['product_id'] = product_data
                    else:
                        Response({'product product not found'})
                return Response(data)
            except Exception as e:
                print(e, item['product_id'])
    except SaleOrderLine.DoesNotExist:
        raise NotFound()
@api_view(['GET'])
def getCommandeById(requets, cmd_id):
    try:
        saleorder = SaleOrder.objects.get(id=cmd_id)
        if not saleorder:
            return Response([])
        else:
            cmd_serializer = CommandeSerializer(saleorder)
            return Response(cmd_serializer.data)
        return Response({'OK'})
    except SaleOrder.DoesNotExist:
        raise NotFound()


@api_view(['GET'])
def get_best_sellers(request):
    best_sellers = SaleOrderLine.objects.values('product_id__product_tmpl_id').annotate(
        total_quantity=Sum('qty_conditionnee')).order_by('-total_quantity')
    product_template_ids = [entry['product_id__product_tmpl_id'] for entry in best_sellers]
    best_selling_product_templates = ProductTemplate.objects.filter(id__in=product_template_ids, image__isnull=False)
    serializer = ProductSerializer(best_selling_product_templates, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_depot(request):
    try:
        cursortest.execute('''select distinct pp.depot_name from public.panier_productavailability pp  where pp.depot_name != \'\' ''')
        results = cursortest.fetchall()
        print(results)
        depot_name=[]
        for row in results:
            depot_name.append({
                'region': row[0]
            })
        return Response(depot_name)
    except Exception as e:
        print(e)


