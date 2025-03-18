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
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken




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
    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = LoanUser.objects.get(email=email,password=password)
        except LoanUser.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        # import base64
        # decoded_password = base64.b64decode(user.password).decode('utf-8')

        # if decoded_password != password:
        #     return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        refresh['role'] = user.role
        refresh['user'] = user.id

        print(refresh['user'])
        
        access_token= str(refresh.access_token)
        
        response= Response({
            'access': access_token  
        }, status=status.HTTP_200_OK)
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,  
            secure=False,  
            samesite="None",  
        )
        
        print("refresh",response)
        return response



    
    
    
class RefreshTokenView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        refresh_token = request.COOKIES.get("refresh_token")  
        print("refresh_token",refresh_token)

        if not refresh_token:
            return Response({"error": "Refresh token missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)  
            access_token = str(refresh.access_token) 
            return Response({"access": access_token}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        
    
class UsercreateView(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoanView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        serializer=LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def list(self,request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({"error": "Token missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        token_str = auth_header.split(' ')[1]  # Extract the token part
        token_data = AccessToken(token_str)  # Decode the token
        
        user_id = token_data.get('user')
        role = token_data.get('role')
        user_id = token_data.get('user')
        print("token_data",token_data)
        role = token_data.get('role')
        try:
            user = LoanUser.objects.get(id=user_id)
        except LoanUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if role == "Admin":
            loans = Loan.objects.all()
        else:
            loans = Loan.objects.filter(user=user)
        return Response({
            "status": "success",
            "data": LoanSerializer(loans, many=True).data
        })




    