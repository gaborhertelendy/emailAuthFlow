from rest_framework import serializers
from MyUser.models import User, Workout

from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)

# THICK serializers / Thin Views
# We perform the heavy duty of validation and data transformation here


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:user-detail')

    class Meta:
        model = User
        fields = [
            'url',
            'pk',
            'email',
            'password',
            'display_name',
            'bio',
            'username'
        ]
        read_only_fields = ['bio', 'pk']

    def create(self, validated_data):
        email = validated_data.__getitem__('email')
        display_name = str(email).split('@')[0]
        username = display_name

        validated_data.pop('email')
        validated_data.pop('display_name')
        validated_data.pop('username')
        # Now you have a clean valid email
        # You might want to call an external API or modify another table
        # (eg. keep track of number of accounts registered.) or even
        # make changes to the email format.

        # Once you are done, create the instance with the validated data
        return User.objects.create(email=email, display_name=display_name, username=username, **validated_data)

    # def update(self, instance, validated_data):

    # E-mail has to be unique, although the model already takes care of this, ve validate here too
    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This e-mail is already registered.")
        return value

    # This should be designed properly here (NOT FINISHED)
    def validate_password(self, value):
        if value == "as":
            raise serializers.ValidationError("as is not strong enough")
        password_hash = make_password(value)

        return password_hash


class WorkoutSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:workout-detail')
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Workout
        fields = [
            'url',
            'owner',
            'pk',
            'efficiency',
            'exercises',
            # , 'sets' we might need to collect sets with primarykey related field later
        ]
        read_only_fields = ['owner', 'url', 'pk', 'efficiency']


