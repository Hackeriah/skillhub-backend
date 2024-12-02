from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User  # Import the custom User model
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError

# Signup view
@api_view(['POST'])
def signup(request):
    data = request.data
    try:
        # Ensure the user creation uses custom password hashing method
        user = User.objects.create(
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
        )
        user.set_password(data['password'])  # Using the custom method to hash password
        user.save()  # Save the user after setting the password

        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

    except IntegrityError:
        # Handling cases where email or username already exists
        return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # General error handling
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Login view
@api_view(['POST'])
def login(request):
    data = request.data
    try:
        user = User.objects.get(email=data['email'])  # We are using email for login
        if user.check_password(data['password']):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
