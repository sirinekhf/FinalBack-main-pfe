from rest_framework import serializers

from partners.models import Company
from .models import ProductCategory, ProductPackaging, ProductUOM, ProductFinal, ProductTemplate, Parametres


class ProductFinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFinal
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    ul_name = serializers.SerializerMethodField()
    uom_name = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()

    def get_ul_name(self, product):
        packaging = ProductPackaging.objects.filter(product_tmpl_id=product.id).first()
        if packaging:
            return packaging.ul_name
        return None

    def get_uom_name(self, product):
        uom = product.uom_id
        if uom:
            return uom.name
        return None
    def get_company_name(self, product):
        company = product.company_id
        if company:
            return company.name
        return None
    class Meta:
        model = ProductTemplate
        fields = '__all__'

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class ParametresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parametres
        fields = '__all__'