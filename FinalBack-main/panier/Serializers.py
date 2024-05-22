from rest_framework import serializers
from panier.models import SaleOrder, SaleOrderLine, ProductProduct
from products.models import ProductTemplate
from users.serializers import UserSerializer


class CartItemSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=ProductTemplate.objects.all())
    qty_cond = serializers.IntegerField()

    def create(self, validated_data):
        product = validated_data['product']
        qty_cond = validated_data['qty_cond']


class CommandeSerializer(serializers.ModelSerializer):
    user_partner = UserSerializer()
    adresse = serializers.SerializerMethodField()
    def get_adresse(self, order):
        if order.partner_id:
            return order.partner_id.street
        return None
    class Meta:
        model = SaleOrder
        fields = '__all__'
class SaleOrderLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = SaleOrderLine
        fields = '__all__'
class ProductProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductProduct
        fields = '__all__'
