import os

from django.contrib.auth.forms import PasswordResetForm
from SalveTempo.settings import EMAIL_HOST_USER, TEMPLATES_ROOT
from django.utils.translation import gettext as _

from rest_framework import serializers

from .models import *

class UserSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'confirm_password']
        extra_kwargs = {
                'password': {'write_only': True}
        }
    
    def save(self):
        user = User(
                email=self.validated_data['email'],
                username=self.validated_data['username']
            )
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Senhas devem ser iguais.'})
        user.set_password(password)
        user.save()
        return user

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_("Dados de e-mail inválidos."))

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("E-mail não cadastrado no sistema."))
        return value

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': EMAIL_HOST_USER,

            'email_template_name': os.path.join(TEMPLATES_ROOT, "account", "email", "reset_password_message.txt"),

            'request': request,
        }
        self.reset_form.save(**opts)