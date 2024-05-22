import psycopg2
from django.http import HttpResponse
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from partners.models import ResLocalite, ResCountry, ResCountryState, Partners
from partners.serializers import PartnerSerializer, CountryStateSerializer, ResLocaliteSerializer
from rest_framework.views import APIView

from users.models import User


connect= psycopg2.connect(user="postgres",
                              password="limil1000",
                              host="localhost",
                              port="5432",
                              database="db1")
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
def importCountry(request):
    cursortest.execute('SELECT id, code ,name FROM public.res_country')
    data = cursortest.fetchall()
    for row in data:
        country = ResCountry(id=row[0], code=row[1], name=row[2])
        country.save()
    return HttpResponse("Import done.")


def importState(request):
    cursortest.execute('SELECT id, code ,name, country_id, region FROM public.partners_rescountrystate pr')
    data = cursortest.fetchall()

    for row in data:
        cid = row[3]
        country = ResCountry.objects.filter(id=cid).first()
        City = ResCountryState(id=row[0], code=row[1], name=row[2], country=country, region=row[4])
        City.save()
    return HttpResponse("done.")


def importLocalite(request):
    cursortest.execute('SELECT * FROM public.res_localite')
    data = cursortest.fetchall()

    for row in data:
        localite = ResLocalite(id=row[0], create_uid=row[1], create_date=row[2], name=row[3], write_uid=row[4],
                               write_date=row[5], localite_code=row[6], code_ville=row[7])
        localite.save()
    return HttpResponse("done.")


class editPartner(APIView):
    def patch(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            user_id = user.id
            partner = Partners.objects.filter(user_id=user_id).first()

        except User.DoesNotExist:
            return Response({'error': f'User with email {email} not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            if request.data.get('name') is not None and request.data['name'].strip() != '':
                partner.name = request.data['name'],
                user.name = request.data['name']

            if request.data.get('phone') is not None and request.data['phone'].strip() != '':
                partner.phone = request.data['phone']
                user.phone = request.data['phone']
            if request.data.get('street') is not None and request.data['street'].strip() != '':
                partner.street = request.data['street']

            if request.data.get('street2') is not None and request.data['street2'].strip() != '':
                partner.street2 = request.data['street2']

            ''' if request.data.get('zip') is not None and request.data['zip'].strip() != '':
                partner.zip = request.data['zip']
    
            if request.data.get('country_id') is not None and request.data['country_id'].strip() != '':
                partner.country_id = ResCountry.objects.filter(id = request.data['country_id']).first()
            '''
            if request.data.get('localite_id') is not None and request.data['localite_id'] != '':
                partner.localite_id = ResLocalite.objects.filter(id = request.data['localite_id']).first()

            if request.data.get('state_id') is not None and request.data['state_id'] != '':
                partner.state_id = ResCountryState.objects.filter(code=request.data['state_id']).first()
    
            user.save()
            partner.save()
            
        except Exception as e:
            print(e)
        return Response({'id': user_id})
@api_view(['GET'])
def getWilaya(request):
    wilaya = ResCountryState.objects.all()
    wilaya_serialized = CountryStateSerializer(wilaya, many=True)
    return Response(wilaya_serialized.data)

@api_view(['GET'])
def getCommune(request, code):
    commune = ResLocalite.objects.filter(code_ville=code)
    commune_serialized = ResLocaliteSerializer(commune, many=True)
    return Response(commune_serialized.data)
@api_view(['GET'])
def getPartnerfromUser(request, user_id):
    user = User.objects.filter(id = user_id).first()
    if user:
        partner = Partners.objects.filter(user_id = user).first()
        if partner:
            partner_serializer = PartnerSerializer(partner)
            return Response(partner_serializer.data)
        else:
            return HttpResponse('Partner doesn\'t exist')
    else:
        return HttpResponse('User doesn\'t exist')


@api_view(['GET'])
def getWilayaById(request, id):
    wilaya = ResCountryState.objects.filter(id = id).first()
    wilaya_serialized = CountryStateSerializer(wilaya)
    return Response(wilaya_serialized.data)

@api_view(['GET'])
def getCommuneById(request, id):
    commune = ResLocalite.objects.filter(id = id).first()
    commune_serialized = ResLocaliteSerializer(commune)
    return Response(commune_serialized.data)
