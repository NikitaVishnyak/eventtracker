from rest_framework import serializers

from users.models import CustomUsers


class CustomUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUsers
        fields = ('first_name', 'last_name', 'email')
