from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import*
from .serializers import*
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from datetime import datetime, timedelta
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny





# def calculate_loan(amount, tenure, interest_rate):
#     """
#     Calculate Monthly EMI, Total Interest, and Total Amount Payable
#     """
#     if amount <= 0 or tenure <= 0 or interest_rate <= 0:
#         raise ValueError("Amount, tenure, and interest rate must be positive values.")

#     monthly_interest_rate = Decimal(interest_rate) / Decimal(100) / 12
#     try:
#         emi = (amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure) / (
#             (1 + monthly_interest_rate) ** tenure - 1
#         )
#     except ZeroDivisionError:
#         emi = amount  # For tenure = 1 month with high interest, set EMI as full amount

#     total_amount = emi * tenure
#     total_interest = total_amount - amount

#     return {
#         "monthly_installment": round(emi, 2),
#         "total_interest": round(total_interest, 2),
#         "total_amount": round(total_amount, 2),
#     }




class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email,password=password)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        # import base64
        # decoded_password = base64.b64decode(user.password).decode('utf-8')

        # if decoded_password != password:
        #     return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        refresh['role'] = user.role
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


    