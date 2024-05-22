from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from partners.models import Partners
from partners.serializers import PartnerSerializer
from .models import User
from users.serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.core.mail import send_mail
from django.http import HttpResponseServerError
# Create your views here.
class registerView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
                try:
                    print('OK')
                    user = serializer.save()
                    if user.is_client_groupe or user.is_client_particulier:
                        createPartner(serializer.data['name'], serializer.data['email'], serializer.data['phone'], user, datetime.datetime.now())
                except Exception as e:
                    print(e)
                return Response(serializer.data)
        else:
            return Response(serializer.errors)

def createPartner(name, email, phone,user, datecreate):
    partner = Partners(name=name,email=email, notify_email=email, state='validate', phone=phone, user_id=user, create_date=datecreate)
    partner.save()

class loginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User n'existe pas ! ")
        if not user.check_password(password):
            raise AuthenticationFailed('Mot de passe incorrect ! ')

        #Creating Tokens JWT
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60), #how long this user could be connected
            'iat': datetime.datetime.utcnow() #the date the tocken is created
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        #set this token via cookies
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}
        return response

class logoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logout success'
        }
        return response

#get the token to authentificate the user
class userView(APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthentified')
        try:
            payload=jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Connexion expiré')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

@api_view(['GET'])
def getComercial(request):
    comercial = User.objects.filter(Q(is_comercial=True) | Q(is_admin=True))
    serializer = UserSerializer(comercial, many=True)
    return Response(serializer.data)
def sendemail(request, subject, msg, receiver):
    try:
        send_mail(subject, msg, 'raniachahinezabbaci@gmail.com', [receiver], fail_silently=False)
        return render(request, 'sendemail.html')
    except Exception as e:
        return HttpResponseServerError(f"An error occurred while sending the email: {str(e)}")

@api_view(['GET'])
def getUsers(request):
    comercial = User.objects.filter(Q(is_client_groupe=True) | Q(is_client_particulier=True))
    serializer = UserSerializer(comercial, many=True)
    return Response(serializer.data )

@api_view(['PATCH'])
def changeaccess(request, id):
    comercial = User.objects.get(id = id)
    state = comercial.is_active
    comercial.is_active = not state
    comercial.is_new= False
    comercial.save()
    serializer = UserSerializer(comercial)
    state = comercial.is_active
    try:
        email = comercial.email
        if state:
            etat =  'activé'
        else:
            etat= 'désactivé'
        sendemail(request, 'Hasnaoui Groupe',
                  f'Cher client votre compte est est {etat}.'
                  f'Cordialement.', email)
    except Exception as e:
        print(e)

    return Response(serializer.data)

@api_view(['GET'])
def getuserbyid(request, id):
    comercial = User.objects.get(id=id)
    partner = Partners.objects.get(user_id = id)

    serializer = UserSerializer(comercial)
    serializer2 = PartnerSerializer(partner)
    data = {
        'user': serializer.data,
        'partner':serializer2.data,
    }
    return Response(data)



