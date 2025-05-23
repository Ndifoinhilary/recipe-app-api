from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user object
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}


    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        :param validated_data:
        :return:
        """
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        :param instance:
        :param validated_data:
        :return:
        """
        password = self.validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user



class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for the user authentication object
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        :param attrs:
        :return:
        """
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs

