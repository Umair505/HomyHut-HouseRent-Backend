from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserAccount

# ✅ Serializer for UserAccount Details
class UserAccountSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username if obj.user else None

    class Meta:
        model = UserAccount
        fields = ['id', 'username', 'profile_image']


# ✅ Serializer for User Registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def validate(self, data):
        """ Ensure both passwords match """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'error': "Passwords do not match"})
        return data

    def create(self, validated_data):
        """ Create and return a new user with hashed password """
        validated_data.pop('confirm_password')  # Remove confirm_password before saving
        user = User.objects.create_user(**validated_data)
        user.is_active = False  # User must verify email first
        user.save()
        return user


# ✅ Serializer for User Login
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


# ✅ Serializer for User Profile Update
class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.CharField(source='account.profile_image', allow_null=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_image']

    def update(self, instance, validated_data):
        """ Update user profile """
        account_data = validated_data.pop('account', {})
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        if account_data:
            instance.account.profile_image = account_data.get('profile_image', instance.account.profile_image)
            instance.account.save()
        
        return instance


# ✅ Serializer for Listing All Users (Admin Only)
class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


# ✅ Serializer for Admin Message System
class AdminMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'


# ✅ Serializer for Managing Staff Users
class UserStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_staff', 'is_superuser']
