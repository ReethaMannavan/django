from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ProfileSerializerV1, ProfileSerializerV2
from django.contrib.auth.models import User

# Registration
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ProfileSerializerV1(data=request.data)  # Can use V1 serializer for creation
        if serializer.is_valid():
            user = serializer.save()
            # Return token immediately
            from rest_framework.authtoken.models import Token
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "username": user.username,
                "email": user.email,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Profile v1
class ProfileViewV1(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializerV1(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializerV1(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Profile v2 (advanced)
class ProfileViewV2(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializerV2(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializerV2(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
