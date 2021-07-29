from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'username', 'bio', 'profile_pic')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        username = f'{instance.first_name}.{instance.last_name}'
        username.replace(' ', '')
        counter = 1
        while User.objects.filter(username=username):
            username += str(counter)
            counter += 1
        instance.username = username

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
