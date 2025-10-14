from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "bio", "profile_image", "groups", "is_staff"]
        read_only_fields = ["is_staff"]
    
    def get_groups(self, obj):
        """Return list of group names"""
        return [group.name for group in obj.groups.all()]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default='author')

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]

    def create(self, validated_data):
        """
        Create user with specified role.
        Signal will automatically set is_staff and add to group.
        """
        role = validated_data.get('role', 'author')
        
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            role=role
        )
        
        # Signal handles group assignment and is_staff
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Separate serializer for updating user profile"""
    
    class Meta:
        model = User
        fields = ["bio", "profile_image"]
        
    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.save()
        return instance