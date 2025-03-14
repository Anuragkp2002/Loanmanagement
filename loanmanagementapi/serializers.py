from .models import*
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model=Loan
        fields="__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"

