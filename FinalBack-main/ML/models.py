from django.db import models
from rest_framework_jwt.serializers import User

from products.models import ProductTemplate


class FrequentItemset(models.Model):
    itemset = models.TextField()
    support = models.FloatField()

class Vente(models.Model):

    produit = models.ForeignKey(ProductTemplate, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField() #qty de ce produit dans la cmd
    montant = models.DecimalField(max_digits=10, decimal_places=2)#montant de ce produit dans la cmd
    date = models.DateField() #date de vente : date de confirmation de commande par admin? date de payement de cmd?

class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductTemplate, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Visitor(models.Model):
    ip_address = models.CharField(max_length=255, null=True)
    date_visited = models.DateTimeField(auto_now_add=True)