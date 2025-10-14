from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, UserUpdateSerializer

User = get_user_model()


class RegisterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user registration.
    POST /api/accounts/register/ - Create new user
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post']  # Only allow POST
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Return success response with user info
        return Response({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_staff': user.is_staff
            }
        }, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing users.
    GET /api/accounts/users/ - List all users
    GET /api/accounts/users/{id}/ - Get specific user
    GET /api/accounts/users/me/ - Get current user profile
    PATCH /api/accounts/users/me/ - Update current user profile
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Optionally filter users based on role.
        Admins and Editors see all users.
        Authors only see themselves.
        """
        user = self.request.user
        
        # Superusers and admins see everyone
        if user.is_superuser or user.groups.filter(name='Admin').exists():
            return User.objects.all()
        
        # Editors see all users
        if user.groups.filter(name='Editor').exists():
            return User.objects.all()
        
        # Authors only see themselves
        return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        """
        Get or update current user's profile.
        GET /api/accounts/users/me/
        PATCH /api/accounts/users/me/
        """
        user = request.user
        
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        
        elif request.method == 'PATCH':
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(UserSerializer(user).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)