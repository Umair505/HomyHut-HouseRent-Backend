from rest_framework import serializers
from .models import RentAdvertisement, RentRequest

class RentAdvertisementSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)  # Make image optional
    class Meta:
        model = RentAdvertisement
        fields = '__all__'
        read_only_fields = ['user', 'status']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class RentRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    ad = serializers.PrimaryKeyRelatedField(queryset=RentAdvertisement.objects.all())

    class Meta:
        model = RentRequest
        fields = ['id', 'ad', 'user', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_ad(self, value):
        # Ensure the user is not requesting their own advertisement
        if value.user == self.context['request'].user:
            raise serializers.ValidationError("You cannot send a rent request for your own advertisement.")
        
        # Ensure the advertisement is approved
        if value.status != 'approved':
            raise serializers.ValidationError("This advertisement is not approved.")
        
        # Ensure the advertisement is available
        if not value.is_available:
            raise serializers.ValidationError("This advertisement is not available for rent.")
        
        return value