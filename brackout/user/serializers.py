from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .acount_activation import AcountActivation


class UserSerializer(serializers.ModelSerializer):
    ''' Serializer for User Model '''
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name', 'gender',
                'birth_date', 'age', 'date_joined', 'is_joined_recently',
                'auth_provider', 'is_active', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True}
        }

    def create(self, validated_data):
        ''' Create a user with encrypted password and return it '''
        new_user = get_user_model().objects.create_user(**validated_data)
        new_user.is_active = False
        new_user.save()

        activator = AcountActivation(self.context['request'], new_user)
        activator.send_email()

        return new_user

    def update(self, instance, validated_data):
        ''' Update and return a user '''
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    ''' Serializer for the user authentication object '''
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        ''' Validate and authenticate user '''
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class OAuthSerializer(serializers.Serializer):
    '''Serializer for OAuth'''
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    name = serializers.CharField()
    auth_provider = serializers.CharField()

    def create(self, validated_data):
        ''' Create a user with encrypted password and return it '''
        new_user = get_user_model().objects.create_user(**validated_data)
        new_user.save()

        return new_user
