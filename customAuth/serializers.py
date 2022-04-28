from rest_framework import serializers
from django.conf import settings
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from customAuth.models import User,AdminProfile,Payee
from django.utils import timezone


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')
   

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_syestem_admin=validated_data['is_syestem_admin'],
            is_tenant=validated_data['is_tenant'],
            is_employee=validated_data['is_employee']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


class AdminProfileSerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = AdminProfile
        exclude = ['added_by']
class PayeeSerializers(serializers.ModelSerializer):
    # total_units = serializers.IntegerField(default=0)
    added_on = serializers.DateTimeField(
    format=None, default=serializers.CreateOnlyDefault(timezone.now))
    
    class Meta:
        model = Payee
        exclude = ['added_by']