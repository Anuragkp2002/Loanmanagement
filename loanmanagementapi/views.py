


from datetime import datetime, timedelta
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
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user=request.user
        print("User:", user)  

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoanView(APIView):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user=request.user
        last_loan = Loan.objects.order_by('-id').first()
        if last_loan and last_loan.loan_id:
            last_id_num = int(last_loan.loan_id.replace("LOAN", ""))
        else:
            last_id_num = 0

        loan_id = f"LOAN{last_id_num + 1:03d}"  

        try:
            amount = float(data.get('amount'))
            tenure = int(data.get('tenure'))  
            annual_interest = data.get('interest')
            print("annual_interest",annual_interest)
        except (TypeError, ValueError):
            return Response({"error": "Invalid amount, tenure, or interest"}, status=400)

        monthly_interest_rate = annual_interest / 100 / 12

        # Calculate EMI
        r = monthly_interest_rate
        n = tenure
        P = amount

        if r == 0:
            emi = P / n
        else:
            emi = P * r * (1 + r) ** n / ((1 + r) ** n - 1)
        emi = round(emi, 2)

        total_amount = round(emi * n, 2)
        total_interest = round(total_amount - P, 2)

        # Generate payment schedule
        today = datetime.today()
        schedule = []
        for i in range(tenure):
            due_date = (today + timedelta(days=30 * (i + 1))).date()
            schedule.append({
                "installment_no": i + 1,
                "due_date": due_date.isoformat(),
                "amount": emi
            })

        
        full_data = {
            **data,
            "loan_id":loan_id,
            "monthly_installment": emi,
            "total_interest": total_interest,
            "total_amount": total_amount,
            "interest_rate": annual_interest,
            "user":user.id
        }

        serializer = LoanSerializer(data=full_data)
        if serializer.is_valid():
            loan_user = serializer.save()

            return Response({
                "status": "success",
                "data": {
                    **serializer.data,
                    "payment_schedule": schedule
                }
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


