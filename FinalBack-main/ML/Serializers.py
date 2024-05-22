
from rest_framework import serializers
from ML.models import FrequentItemset

class FrequentItemsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequentItemset
        fields = ['itemset', 'support']