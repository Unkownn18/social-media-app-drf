from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['email','username','password','confirm_password']

    def validate(self,data):
        if data['password']!=data['confirm_password']:
            raise serializers.ValidationError('Password do not match')
        return data
    def create(self, validated_data):
        password=validated_data.pop('confirm_password')
        user=User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(write_only=True)
    password=serializers.CharField(write_only=True)
    
    def validate(self, data):
        user=User.objects.filter(username=data['username']).first()
        if user and user.check_password(data['password']):
            refresh=RefreshToken.for_user(user=user)
            return(
                {
                    'refresh':str(refresh),
                    'access':str(refresh.access_token)
                }
            )
        raise serializers.ValidationError('Invalid Credentials')