from rest_framework import serializers

from .models import Partners, ResCountryState, ResLocalite


class PartnerSerializer(serializers.ModelSerializer):
    wilaya = serializers.SerializerMethodField()
    commune = serializers.SerializerMethodField()
    code_ville = serializers.SerializerMethodField()

    def get_wilaya(self, partner):
        state = partner.state_id

        if state:
            return state.name
        return None
    def get_code_ville(self, partner):
        state = partner.state_id
        if state:
            return state.code
        return None

    def get_commune(self, partner):
        commune = partner.localite_id
        if commune:
            return commune.name
        return None
    class Meta:
        model = Partners
        fields = '__all__'

class CountryStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResCountryState
        fields = '__all__'

class ResLocaliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResLocalite
        fields = '__all__'
