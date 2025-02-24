from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Show username instead of ID
    
    class Meta:
        model = Review
        fields = ['id', 'ad', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']  # Prevent user from editing these fields

    

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)