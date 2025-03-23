# from django.shortcuts import render
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.exceptions import AuthenticationFailed
# from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from .models import *
# from .serializers import *

# class LoginViewSet(viewsets.ViewSet):
#     permission_classes = [AllowAny]

#     def create(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         try:
#             user = LoanUser.objects.get(email=email, password=password)

#         except LoanUser.DoesNotExist:
#             return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

#         refresh = RefreshToken.for_user(user)
#         refresh['role'] = user.role
#         # refresh['id'] = user.id

       

#         access_token = str(refresh.access_token)

#         response = Response({
#             'access': access_token
#         }, status=status.HTTP_200_OK)
#         response.set_cookie(
#             key="refresh_token",
#             value=str(refresh),
#             httponly=True,
#             secure=False,
#             samesite="None",
#         )
#         return response


# class RefreshTokenView(viewsets.ViewSet):
#     permission_classes = [AllowAny]

#     def create(self, request):
#         refresh_token = request.COOKIES.get("refresh_token")

#         if not refresh_token:
#             return Response({"error": "Refresh token missing"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             refresh = RefreshToken(refresh_token)
#             access_token = str(refresh.access_token)
#             return Response({"access": access_token}, status=status.HTTP_200_OK)
#         except Exception:
#             return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


# class UserCreateView(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     def create(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message": "User created successfully", "data": serializer.data},
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoanView(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def extract_token_data(self, request):
#         """Extract and return token data."""
#         try:
#             token_str = request.headers.get('Authorization').split(' ')[1]
#             token_data = AccessToken(token_str)
#             return {
#                 'role': token_data.get('role'),
#                 # 'user_id': token_data.get('user_id')
#             }
#         except Exception:
#             raise AuthenticationFailed('Invalid or expired token')

#     def create(self, request):
#         serializer = LoanSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "status": "success",
#                 "data": serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def list(self, request):
#         token_data = self.extract_token_data(request)
#         role = token_data.get('role')
#         user_id = token_data.get('user_id')

#         try:
#             user = LoanUser.objects.get(id=user_id)
#         except LoanUser.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         loans = Loan.objects.all() if role == "Admin" else Loan.objects.filter(user=user)

#         return Response({
#             "status": "success",
#             "data": LoanSerializer(loans, many=True).data
#         })







from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from .serializers import *





def get_tokens_for_user(loanuser):
    refresh = RefreshToken.for_user(loanuser)
    refresh['role'] = loanuser.role
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            loanuser = LoanUser.objects.get(email=email, password=password)
        except LoanUser.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens_for_user(loanuser)
        return Response({
            **tokens,
        }, status=status.HTTP_200_OK)



class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "Refresh token missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({"access": access_token}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


class UserCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Headers:", request.headers)
        print("User:", request.user)  
        print("Auth:", request.auth)
        

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoanView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            loan_user = serializer.save()

            tokens = get_tokens_for_user(loan_user)

            return Response({
                "status": "success",
                "data": serializer.data,
                # "tokens": tokens  # Return tokens in response
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        
        
        user_id = request.user.id

        try:
            user = LoanUser.objects.get(id=user_id)
            role=user.role
        except LoanUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        loans = Loan.objects.all() if role == "Admin" else Loan.objects.filter(user=user)

        return Response({
            "status": "success",
            "data": LoanSerializer(loans, many=True).data
        })


