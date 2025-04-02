#from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from Userapp.models import UserDetails
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = UserDetails
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length':8},
        }
        
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError({'error': 'Password and password2 must be same'})
        
        if UserDetails.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = UserDetails(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
        
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")  # Use username instead of email
        password = attrs.get("password")

        if not username or not password:
            raise serializers.ValidationError({"error": "Both username and password are required."})

        # Authenticate the user with username
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError({"error":"No active account found with the given credentials."})

        # Generate token
        data = super().validate(attrs)
        data["username"] = user.username# Add username to the response
        data["email"] = user.email
        return data
       


# from rest_framework import serializers
# from Userapp.models import User
# from django.contrib.auth import authenticate 


# class RegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=50, write_only=True)
#     password2 = serializers.CharField(max_length=50, write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'password2']

#     def validate(self, attrs):
#         password = attrs.get('password')
#         confirm_password = attrs.get('password2')

#         if password != confirm_password:
#             raise serializers.ValidationError("Passwords do not match.")
#         return attrs

#     def create(self, validated_data):
#         validated_data.pop('password2')  # Remove confirm_password before creating user
#         return User.objects.create_user(**validated_data)


# class LoginSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(max_length=255)
#     password = serializers.CharField(max_length=128, write_only=True)
#     tokens = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ['username', 'password', 'tokens']

#     def get_tokens(self, obj):
#         user = User.objects.get(username=obj['username'])
#         return user.tokens()

#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')

#         user = authenticate(username=username, password=password)
#         if not user:
#             raise serializers.ValidationError("Invalid credentials.")
#         if not user.is_active:
#             raise serializers.ValidationError("Account is disabled. Contact admin.")
#         return {'username': user.username, 'tokens': user.tokens()}



# from Userapp.models import CustomUser
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework import serializers

# # Custom JWT Serializer to include additional fields in the token
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['username'] = user.username
#         token['email'] = user.email
#         return token

# # Registration Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'password', 'password2']
#         extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

#     def save(self, **kwargs):
#         password = self.validated_data['password']
#         password2 = self.validated_data['password2']
#         if password != password2:
#             raise serializers.ValidationError({'error': 'Passwords do not match'})

#         if CustomUser.objects.filter(email=self.validated_data['email']).exists():
#             raise serializers.ValidationError({'error': 'Email already exists'})

#         user = CustomUser(
#             email=self.validated_data['email'],
#             username=self.validated_data['username'],
#         )
#         user.set_password(password)
#         user.save()
#         return user



