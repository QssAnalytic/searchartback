from rest_framework import serializers
from .models import CustomUser
from rest_framework.parsers import JSONParser

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name','gender',
                  'company','industry','job_title','phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        if validated_data.get('gender'):
            user.gender=validated_data.get('gender')
        if validated_data.get('company'):
            user.company=validated_data.get('company')
        if validated_data.get('industry'):
            user.industry=validated_data.get('industry')
        if validated_data.get('job_title'):
            user.job_title=validated_data.get('job_title')
        if validated_data.get('phone_number'):
            user.phone_number=validated_data.get('phone_number')
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
