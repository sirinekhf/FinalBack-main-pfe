from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_jwt.serializers import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed

@api_view(['GET']) #add it so that we can use reponse method
def getRoutes(request):
    routes=[
        'api/token', #where submit username and password and get back a access token
        'api/token/refresh',
    ]
    return Response(routes)


#to obtain user information from the access token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if user is not None:
            if user.is_comercial:
                type = 'comercial'
            elif user.is_client_groupe:
                type = 'groupe'
            elif user.is_client_particulier:
                type = 'particulier'
            elif user.is_admin:
                type = 'admin'
        token['username'] = user.name
        token['active'] = user.is_active
        token['name'] = user.name
        token['email'] = user.email
        token['type'] = type
        token['phone'] = user.phone

        return token

    def validate(self, attrs):
        type=''
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                if not check_password(password, user.password):
                    raise AuthenticationFailed("Mot de passe incorrect !")
                if not user.is_active:
                    raise AuthenticationFailed("Ce compte est désactivé !")
            except User.DoesNotExist:
                raise AuthenticationFailed("Cette utilisateur n'existe pas !")

            if user is not None:
                if user.is_comercial:
                    type = 'comercial'
                elif user.is_client_groupe:
                    type = 'groupe'
                elif user.is_client_particulier:
                    type = 'particulier'
                elif user.is_admin:
                    type = 'admin'
        else:
            raise AuthenticationFailed('L\'email et le mot de passe sont obligatoires', code='authentication')

        refresh = self.get_token(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.name,
            'type': type
        }
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

'''
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            raise AuthenticationFailed('L\'email et le mot de passe sont obligatoires')

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("L'utilisateur n'existe pas")

        if not user.check_password(password):
            raise AuthenticationFailed('Mot de passe incorrect')

        serializer = self.get_serializer(user)
        refresh = RefreshToken.for_user(user)  # generate refresh token

        response_data = {
            'refresh': str(refresh),
            'access': str(serializer.data['access']),
        }

        return Response(response_data)'''