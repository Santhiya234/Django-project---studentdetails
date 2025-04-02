from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from Userapp.api.serializers import RegisterSerializer, CustomTokenObtainPairSerializer

#mail send for reset password
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({
                'refresh': serializer.validated_data['refresh'],
                'access': serializer.validated_data['access'],
                'username': serializer.validated_data['username'],
                'message': 'Login successful',
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"})
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()        
class ForgotPasswordView(APIView):
    def post(self, request):
        username = request.data.get("username")
        if not username:
            return Response({'error': "Username is required to reset password"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status = status.HTTP_404_NOT_FOUND)
        
        #generate password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = request.build_absolute_uri(reverse('reset-password', kwargs={"uidb64": uid, "token": token}))
        #send reset mail
        send_mail(
            "Password reset request",
            f"Click the link to reset your password: {reset_url}",
            "example1@gmail.com",
            [user.email],
            fail_silently=False,
        )
        
        return Response({'message': "Reset link send successfully"}, status=status.HTTP_200_OK)
    
class ResetPasswordView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(User.DoesNotExist, ValueError):
            return Response({'error': "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)
        
        #validate token
        if not default_token_generator.check_token(user, token):
            return Response({'error': "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        
        if not new_password or new_password != confirm_password:
            return Response({'error': "passwords do not match"}, status= status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'message':"Password reset successfully"}, status=status.HTTP_200_OK)
    
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from Userapp.models import User
# from Userapp.api.serializers import RegistrationSerializer, LoginSerializer


# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.validated_data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken
# from Userapp.api.serializers import CustomTokenObtainPairSerializer, RegisterSerializer

# # Registration View
# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Custom Login View using JWT
# class LoginView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
    

# # Logout View
# class LogoutView(APIView):
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()  # Blacklist the refresh token
#             return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


