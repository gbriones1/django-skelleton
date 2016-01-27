from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    # groups = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     view_name='group-detail',
    #     queryset=Group.objects.all()
    # )
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.ModelSerializer):
    # user_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ('url', 'name', 'user_set')
