from rest_framework import serializers
from .models import Favorite
from rent.serializers import RentAdvertisementSerializer

class FavoriteSerializer(serializers.ModelSerializer):
    ad_details = RentAdvertisementSerializer(source='ad', read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'ad', 'ad_details', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)