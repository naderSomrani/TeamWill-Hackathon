from rest_framework import serializers
from .models import *


class TypeCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCredit
        fields = '__all__'


class DocCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocCredit
        fields = '__all__'


class ChampCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChampCredit
        fields = '__all__'


class DossierProspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DOSSIERPROSPECT
        fields = '__all__'


class DPRCCRValeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = DPRCCRVALEUR
        fields = '__all__'


class DPRECHEANCESerializer(serializers.ModelSerializer):
    class Meta:
        model = DPRECHEANCE
        fields = '__all__'


class DemandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DOCUMENTDEMANDE
        fields = '__all__'


class DEMANDECREDITSerializer(serializers.ModelSerializer):
    class Meta:
        model = DEMANDECREDIT
        fields = '__all__'

# class RegisterSerializer(RegisterSerializer):
#     PRONOM = serializers.CharField(required=True, write_only=True)
#     PROPRENOM = serializers.CharField(required=True, write_only=True)
#     PRODEPRENOM = serializers.CharField(required=True, write_only=True)
#     #PRODATENAISS = serializers.DateField(required=False)
#     PROMAIl = serializers.CharField(required=True, write_only=True)
#     PROTEL = serializers.CharField(required=True, write_only=True)
#     username = serializers.CharField(required=True, write_only=True)
#     password1 = serializers.CharField(required=True, write_only=True)
#     password2 = serializers.CharField(required=True, write_only=True)
#
#     def validate_email(self, email):
#         email = get_adapter().clean_email(email)
#         if allauth_settings.UNIQUE_EMAIL:
#             if email and email_address_exists(email):
#                 raise serializers.ValidationError(
#                     ("A user is already registered with this e-mail address."))
#         return email
#
#     def validate_password1(self, password):
#         return get_adapter().clean_password(password)
#
#     def validate(self, data):
#         if data['password1'] != data['password2']:
#             raise serializers.ValidationError(
#                 ("The two password fields didn't match."))
#         return data
#
#     def get_cleaned_data(self):
#         super(RegisterSerializer, self).get_cleaned_data()
#         return {
#             'username': self.validated_data.get('username', ''),
#             'password1': self.validated_data.get('password1', ''),
#             'PRONOM': self.validated_data.get('PRONOM', ''),
#             'PROPRENOM': self.validated_data.get('PROPRENOM', ''),
#             'PRODEPRENOM': self.validated_data.get('PRODEPRENOM', ''),
#             #'PRODATENAISS': self.validated_data.get('PRODATENAISS', ''),
#             'PROMAIl': self.validated_data.get('PROMAIl', ''),
#             'PROTEL': self.validated_data.get('PROTEL', ''),
#         }
#
#     def save(self, request):
#         adapter = get_adapter()
#         user = adapter.new_user(request)
#         self.cleaned_data = self.get_cleaned_data()
#         adapter.save_user(request, user, self)
#         setup_user_email(request, user, [])
#         user.username = self.cleaned_data.get('username')
#         user.PRONOM = self.cleaned_data.get('PRONOM')
#         user.PROPRENOM = self.cleaned_data.get('PROPRENOM')
#         user.PRODEPRENOM = self.cleaned_data.get('PRODEPRENOM')
#         #user.PRODATENAISS = self.cleaned_data.get('PRODATENAISS')
#         user.PROMAIl = self.cleaned_data.get('PROMAIl')
#         user.PROTEL = self.cleaned_data.get('PROTEL')
#
#         user.save()
#         return user
